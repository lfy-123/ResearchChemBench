from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from json_repair import repair_json
from jsonschema import ValidationError, validate

from src.agents.workspace import isolated_environment, remove_agent_credentials
from src.core.io import write_json, write_jsonl
from src.core.logging import pipeline_logger

SECRET_PATTERN = re.compile(
    r"(?i)(authorization|api[_-]?key|token|secret|password)([\"'\s:=]+)([^\s\"']+)"
)


def run_agent(
    *,
    cli_config: dict[str, Any],
    paths: dict[str, Path],
    prompt: str,
    response_schema: dict[str, Any],
    label: str,
) -> dict[str, Any]:
    cli = str(cli_config.get("cli") or "opencode").casefold()
    if cli not in {"codex", "claude", "opencode"}:
        raise ValueError(f"unsupported agent CLI: {cli}")
    command = str(cli_config.get("command") or cli)
    executable = shutil.which(command) if Path(command).parent == Path(".") else command
    if not executable or not Path(executable).exists():
        raise FileNotFoundError(f"agent CLI not found: {command}")
    run_root = paths["run_root"]
    prompt_path = run_root / "prompt.md"
    schema_path = run_root / "response_schema.json"
    prompt_path.write_text(prompt, encoding="utf-8")
    write_json(schema_path, response_schema)
    write_json(paths["workspace"] / "response_schema.json", response_schema)
    uses_custom_opencode_provider = cli == "opencode" and bool(
        cli_config.get("base_url") or cli_config.get("url")
    )
    environment = isolated_environment(
        paths,
        cli,
        cli_config.get("environment"),
        copy_cli_auth=not uses_custom_opencode_provider,
    )
    argv, stdin_text = _command(
        cli,
        executable,
        cli_config,
        paths,
        prompt,
        response_schema,
        schema_path,
        environment,
        label,
    )
    native_path = run_root / "native_events.jsonl"
    stderr_path = run_root / "stderr.log"
    stdout_path = run_root / "stdout.log"
    final_path = run_root / "final_response.json"
    started_at = _now()
    started = time.monotonic()
    pipeline_logger().info(
        "AGENT START | label=%s | cli=%s | model=%s", label, cli, cli_config.get("model")
    )
    attempts_root = run_root / "attempts"
    attempts_root.mkdir(parents=True, exist_ok=True)
    attempts: list[dict[str, Any]] = []
    max_attempts = max(1, int(cli_config.get("retries", 2)) + 1)
    stdout = ""
    stderr = ""
    events: list[dict[str, Any]] = []
    return_code = -1
    timed_out = False
    try:
        for attempt_number in range(1, max_attempts + 1):
            attempt_root = attempts_root / f"attempt_{attempt_number:02d}"
            attempt_root.mkdir(parents=True, exist_ok=True)
            attempt_stdout = attempt_root / "stdout.log"
            attempt_stderr = attempt_root / "stderr.log"
            final_path.unlink(missing_ok=True)
            return_code, timed_out = _execute(
                argv,
                cwd=paths["workspace"],
                env=environment,
                stdin_text=stdin_text,
                stdout_path=attempt_stdout,
                stderr_path=attempt_stderr,
                timeout_seconds=int(cli_config.get("timeout_seconds", 1800)),
                heartbeat_label=f"{label}:attempt-{attempt_number}",
            )
            stdout = attempt_stdout.read_text(encoding="utf-8", errors="replace")
            stderr = attempt_stderr.read_text(encoding="utf-8", errors="replace")
            events = _json_events(stdout)
            attempt_error = _execution_error(return_code, timed_out, events, stderr)
            attempts.append(
                {
                    "attempt": attempt_number,
                    "return_code": return_code,
                    "timed_out": timed_out,
                    "error": attempt_error,
                    "stdout_path": str(attempt_stdout),
                    "stderr_path": str(attempt_stderr),
                }
            )
            if not attempt_error or attempt_number >= max_attempts or not _retryable(attempt_error):
                break
            delay = min(2 ** (attempt_number - 1), 8)
            pipeline_logger().warning(
                "AGENT RETRY | label=%s | attempt=%d/%d | delay_seconds=%d | error=%s",
                label,
                attempt_number,
                max_attempts,
                delay,
                attempt_error,
            )
            time.sleep(delay)
    finally:
        remove_agent_credentials(paths["home"])
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    native_path.write_text(_redact(stdout), encoding="utf-8")
    session_id = _find_value(events, ("sessionID", "session_id", "sessionId"))
    usage = _usage(events)
    final_text = _final_text(cli, events, stdout, final_path)
    parsed: dict[str, Any] | None = None
    error: str | None = None
    if timed_out:
        error = "agent timed out"
    elif return_code != 0:
        error = _event_error(events) or _redact(stderr[-4000:]) or f"agent exited {return_code}"
    else:
        try:
            parsed_value = json.loads(repair_json(final_text))
            if not isinstance(parsed_value, dict):
                raise ValueError("agent response must be a JSON object")
            validate(parsed_value, response_schema)
            parsed = parsed_value
            write_json(final_path, parsed)
        except (json.JSONDecodeError, ValidationError, ValueError) as exc:
            error = f"invalid structured response: {exc}"
    conversation = [
        {"role": "user", "content": _redact(prompt)},
        {"role": "assistant", "content": parsed if parsed is not None else _redact(final_text)},
    ]
    write_jsonl(run_root / "conversation.jsonl", conversation)
    result = {
        "status": "success" if parsed is not None and not error else "error",
        "cli": cli,
        "model": cli_config.get("model"),
        "command": _redacted_command(argv),
        "started_at": started_at,
        "finished_at": _now(),
        "duration_seconds": round(time.monotonic() - started, 3),
        "return_code": return_code,
        "timed_out": timed_out,
        "session_id": session_id,
        "usage": usage,
        "attempts": attempts,
        "native_events_path": str(native_path),
        "conversation_path": str(run_root / "conversation.jsonl"),
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
        "final_response_path": str(final_path) if final_path.is_file() else None,
        "parsed_response": parsed,
        "error": error,
    }
    write_json(
        run_root / "run_metadata.json",
        {key: value for key, value in result.items() if key != "parsed_response"},
    )
    pipeline_logger().info(
        "AGENT COMPLETE | label=%s | cli=%s | status=%s | duration_seconds=%.1f",
        label,
        cli,
        result["status"],
        result["duration_seconds"],
    )
    return result


def _command(
    cli: str,
    executable: str,
    config: dict[str, Any],
    paths: dict[str, Path],
    prompt: str,
    schema: dict[str, Any],
    schema_path: Path,
    env: dict[str, str],
    label: str,
) -> tuple[list[str], str | None]:
    model = str(config.get("model") or "")
    if cli == "codex":
        argv = [
            executable,
            "exec",
            "--json",
            "--ephemeral",
            "--ignore-user-config",
            "--sandbox",
            "workspace-write",
            "--output-schema",
            str(schema_path),
            "--output-last-message",
            str(paths["run_root"] / "final_response.json"),
            "-C",
            str(paths["workspace"]),
        ]
        if model:
            argv.extend(["--model", model])
        argv.append("-")
        return argv, prompt
    if cli == "claude":
        argv = [
            executable,
            "--print",
            "--bare",
            "--no-session-persistence",
            "--permission-mode",
            "dontAsk",
            "--tools",
            "Read,Glob,Grep",
            "--output-format",
            "stream-json",
            "--json-schema",
            json.dumps(schema, ensure_ascii=False),
        ]
        if model:
            argv.extend(["--model", model])
        return argv, prompt
    selected_model = _write_opencode_config(paths["workspace"], config, env, model)
    opencode_prompt = (
        f"{prompt}\n\nThe final response must be a single JSON object that validates against "
        "response_schema.json in the workspace root. Do not wrap it in Markdown."
    )
    return (
        [
            executable,
            "run",
            "--pure",
            "--auto",
            "--format",
            "json",
            "--model",
            selected_model,
            "--title",
            label,
            opencode_prompt,
        ],
        None,
    )


def _write_opencode_config(
    workspace: Path, config: dict[str, Any], env: dict[str, str], model: str
) -> str:
    base_url = config.get("base_url") or config.get("url")
    api_key_env = str(config.get("api_key_env") or "JUDGE_API_KEY")
    if not base_url:
        return model
    api_key = os.environ.get(api_key_env) or env.get(api_key_env)
    if not api_key:
        raise RuntimeError(f"missing API key environment variable: {api_key_env}")
    env["RESEARCHCHEMBENCH_AGENT_API_KEY"] = api_key
    model_id = model.split("/", 1)[-1] or "deepseek-v4-flash"
    payload = {
        "$schema": "https://opencode.ai/config.json",
        "enabled_providers": ["researchchembench"],
        "permission": {
            "read": "allow",
            "glob": "allow",
            "grep": "allow",
            "list": "allow",
            "edit": "deny",
            "bash": "deny",
            "task": "deny",
            "todowrite": "deny",
            "external_directory": "deny",
            "webfetch": "deny",
            "websearch": "deny",
        },
        "provider": {
            "researchchembench": {
                "npm": "@ai-sdk/openai-compatible",
                "name": "ResearchChemBench Agent API",
                "options": {
                    "baseURL": str(base_url),
                    "apiKey": "{env:RESEARCHCHEMBENCH_AGENT_API_KEY}",
                },
                "models": {model_id: {"name": model_id}},
            }
        },
    }
    write_json(workspace / "opencode.json", payload)
    return f"researchchembench/{model_id}"


def _execute(
    argv: list[str],
    *,
    cwd: Path,
    env: dict[str, str],
    stdin_text: str | None,
    stdout_path: Path,
    stderr_path: Path,
    timeout_seconds: int,
    heartbeat_label: str,
) -> tuple[int, bool]:
    with (
        stdout_path.open("w", encoding="utf-8") as stdout,
        stderr_path.open("w", encoding="utf-8") as stderr,
    ):
        process = subprocess.Popen(
            argv,
            cwd=cwd,
            env=env,
            stdin=subprocess.PIPE if stdin_text is not None else subprocess.DEVNULL,
            stdout=stdout,
            stderr=stderr,
            text=True,
        )
        if stdin_text is not None and process.stdin:
            process.stdin.write(stdin_text)
            process.stdin.close()
        stop = threading.Event()
        heartbeat = threading.Thread(
            target=_heartbeat,
            args=(stop, heartbeat_label, process.pid),
            daemon=True,
        )
        heartbeat.start()
        try:
            return process.wait(timeout=timeout_seconds), False
        except subprocess.TimeoutExpired:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            return process.returncode or -9, True
        except BaseException:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            raise
        finally:
            stop.set()
            heartbeat.join(timeout=2)


def _heartbeat(stop: threading.Event, label: str, pid: int) -> None:
    while not stop.wait(15):
        pipeline_logger().info("AGENT HEARTBEAT | label=%s | pid=%d", label, pid)


def _json_events(text: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line in text.splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            events.append(value)
    return events


def _final_text(cli: str, events: list[dict[str, Any]], stdout: str, final_path: Path) -> str:
    if cli == "codex" and final_path.is_file():
        return final_path.read_text(encoding="utf-8", errors="replace")
    candidates: list[str] = []
    for event in events:
        for path in (
            ("result",),
            ("structured_output",),
            ("part", "text"),
            ("message", "content"),
            ("content",),
            ("text",),
        ):
            value: Any = event
            for key in path:
                value = value.get(key) if isinstance(value, dict) else None
            if isinstance(value, str) and value.strip():
                candidates.append(value)
            elif isinstance(value, dict):
                candidates.append(json.dumps(value, ensure_ascii=False))
    return candidates[-1] if candidates else stdout.strip()


def _find_value(events: list[dict[str, Any]], keys: tuple[str, ...]) -> Any:
    for event in events:
        value = _recursive_find(event, keys)
        if value is not None:
            return value
    return None


def _recursive_find(value: Any, keys: tuple[str, ...]) -> Any:
    if isinstance(value, dict):
        for key in keys:
            if key in value:
                return value[key]
        for item in value.values():
            found = _recursive_find(item, keys)
            if found is not None:
                return found
    elif isinstance(value, list):
        for item in value:
            found = _recursive_find(item, keys)
            if found is not None:
                return found
    return None


def _usage(events: list[dict[str, Any]]) -> dict[str, Any]:
    for event in reversed(events):
        part = event.get("part") if isinstance(event, dict) else None
        if isinstance(part, dict) and isinstance(part.get("tokens"), dict):
            return part["tokens"]
        usage = event.get("usage") if isinstance(event, dict) else None
        if isinstance(usage, dict):
            return usage
    return {}


def _execution_error(
    return_code: int, timed_out: bool, events: list[dict[str, Any]], stderr: str
) -> str | None:
    if timed_out:
        return "agent timed out"
    if return_code != 0:
        return _event_error(events) or _redact(stderr[-4000:]) or f"agent exited {return_code}"
    return None


def _retryable(error: str) -> bool:
    normalized = error.casefold()
    return any(
        marker in normalized
        for marker in (
            "timeout",
            "timed out",
            "unexpected server error",
            "unknownerror",
            "rate limit",
            "temporarily unavailable",
            "connection reset",
            "connection refused",
            "bad gateway",
            "service unavailable",
        )
    )


def _event_error(events: list[dict[str, Any]]) -> str | None:
    for event in reversed(events):
        if event.get("type") == "error" or event.get("error"):
            return _redact(json.dumps(event.get("error") or event, ensure_ascii=False))[-4000:]
    return None


def _redact(value: str) -> str:
    return SECRET_PATTERN.sub(lambda match: f"{match.group(1)}{match.group(2)}<redacted>", value)


def _redacted_command(argv: list[str]) -> list[str]:
    return [_redact(item) for item in argv]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()
