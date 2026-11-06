"""Gemini-only CLI configuration and exact-session recovery.

No existing harness imports this module unless its agent kind is Gemini.
Credentials remain in the child environment; settings contain no secret values.
"""
from __future__ import annotations

import hashlib
import json
import os
import uuid
from pathlib import Path


def session_home(runner):
    from .recovery import runner_store
    return runner_store(runner).directory / "gemini_home"


def authentication(env):
    selected = env.get("RCB_GEMINI_AUTH_TYPE")
    if not selected:
        selected = "gemini-api-key" if env.get("GEMINI_API_KEY") else (
            "vertex-ai" if env.get("GOOGLE_GENAI_USE_VERTEXAI", "").lower() in {"true", "1"} else "oauth-personal")
    if selected not in {"gemini-api-key", "vertex-ai", "oauth-personal"}:
        raise ValueError("RCB_GEMINI_AUTH_TYPE must be gemini-api-key, vertex-ai or oauth-personal")
    if selected == "gemini-api-key" and not env.get("GEMINI_API_KEY"):
        raise ValueError("Gemini requires GEMINI_API_KEY; an OpenAI API key is not interchangeable")
    if selected == "oauth-personal" and not env.get("GOOGLE_APPLICATION_CREDENTIALS"):
        cached = Path(os.environ.get("GEMINI_CLI_HOME", str(Path.home()))) / ".gemini/oauth_creds.json"
        if not cached.is_file():
            raise ValueError("Gemini credentials missing: set GEMINI_API_KEY or authenticate Gemini CLI first")
        # Gemini can read an existing credential through this documented SDK
        # environment path; do not copy the operator's settings or sessions.
        env["GOOGLE_APPLICATION_CREDENTIALS"] = str(cached)
    return selected


def prepare(runner, env):
    from chemistry_toolbox.src.recovery_io import atomic_json
    auth = authentication(env)
    from .recovery import runner_store, RunRecoveryError
    from urllib.parse import urlsplit
    provider = {"model": runner.gemini_model, "auth_type": auth,
                **{key: env.get(key, "") for key in ("GOOGLE_GEMINI_BASE_URL", "GOOGLE_VERTEX_BASE_URL", "GOOGLE_CLOUD_PROJECT", "GOOGLE_CLOUD_LOCATION")}}
    for key in ("GOOGLE_GEMINI_BASE_URL", "GOOGLE_VERTEX_BASE_URL"):
        if provider[key]:
            url = urlsplit(provider[key])
            if url.scheme not in {"http", "https"} or not url.netloc or url.username or url.password or url.query or url.fragment:
                raise ValueError("Gemini base URL must be HTTP(S), without embedded credentials or query parameters")
    store = runner_store(runner)
    saved = store.get_record("gemini", "provider")
    if saved is not None and saved != provider:
        raise RunRecoveryError("gemini_provider_configuration_drift")
    store.put_record("gemini", "provider", provider, immutable=True)
    home = session_home(runner)
    home.mkdir(parents=True, exist_ok=True, mode=0o700)
    home.chmod(0o700)
    config_dir = home / ".gemini"
    config_dir.mkdir(mode=0o700, exist_ok=True)
    settings = {
        "security": {"auth": {"selectedType": auth}},
        "general": {"enableAutoUpdate": False, "enableAutoUpdateNotification": False},
        "telemetry": {"enabled": False},
        "model": {"name": runner.gemini_model, "maxSessionTurns": runner.max_turns},
        "tools": {"useRipgrep": False, "core": ["read_file", "read_many_files", "list_directory", "glob", "grep_search", "search_file_content", "write_file", "replace"]},
        "mcpServers": {spec["name"]: {
            **({'httpUrl': runner._mcp_connections[spec['name']]['url'], 'headers': runner._mcp_connections[spec['name']]['headers']}
               if getattr(runner, '_mcp_connections', {}).get(spec['name']) else
               {"command": spec["command"][0], "args": spec["command"][1:], "env": spec["environment"]}),
            "timeout": runner.mcp_tool_timeout_ms,
            "trust": True, **({"excludeTools": spec["disabled_tools"]} if spec.get("disabled_tools") else {}),
        } for spec in runner._mcp_server_specs()},
    }
    if runner.auto_compact_token_limit is not None:
        settings["model"]["compressionThreshold"] = runner.auto_compact_token_limit / runner.context_window_tokens
    atomic_json(config_dir / "settings.json", settings)
    # Isolate system and user settings as well as session history.
    atomic_json(home / "empty_settings.json", {})
    env.update(GEMINI_CLI_HOME=str(home), GEMINI_CLI_SYSTEM_SETTINGS_PATH=str(home / "empty_settings.json"),
               GEMINI_CLI_SYSTEM_DEFAULTS_PATH=str(home / "empty_settings.json"), NO_BROWSER="true")
    for name in list(env):
        if any(word in name.upper() for word in ("JUDGE", "SCORER", "EVALUATOR")) or name.startswith(("RCB_CODEX_", "OPENAI_", "ANTHROPIC_")):
            env.pop(name, None)
    return env


def argv(runner):
    command = [runner.agent["executable"], "--model", runner.gemini_model,
               "--output-format", "stream-json", "--approval-mode", "yolo", "--extensions", "none",
               "--allowed-mcp-server-names", *[s["name"] for s in runner._mcp_server_specs()]]
    prompt = runner.instructions_path.read_text(encoding="utf-8")
    if runner._resume_session_id:
        command += ["--resume", runner._resume_session_id]
        prompt = runner._recovery_notice or "Continue the original task using its saved computations."
    return [*command, "--prompt", prompt]


def read_session(runner, *, required=False):
    from .recovery import RunRecoveryError
    sid = runner._resume_session_id
    try:
        uuid.UUID(str(sid))
    except ValueError as exc:
        if required:
            raise RunRecoveryError("gemini_session_id_invalid") from exc
        return None
    home = session_home(runner).resolve()
    matches = []
    for path in (home / ".gemini/tmp").glob("*/chats/session-*.json"):
        if not path.resolve().is_relative_to(home):
            raise RunRecoveryError("gemini_session_path_invalid")
        try:
            data = json.loads(path.read_text())
        except (OSError, ValueError):
            continue  # The CLI may be atomically replacing an active session.
        if data.get("sessionId") == sid:
            expected = hashlib.sha256(str(runner.workspace.resolve()).encode()).hexdigest()
            if data.get("projectHash") != expected:
                raise RunRecoveryError("gemini_session_workspace_mismatch")
            matches.append((path, data))
    if len(matches) == 1:
        return matches[0]
    if required:
        raise RunRecoveryError("gemini_session_missing_or_ambiguous")
    return None


def capture(runner, event):
    from .recovery import RunRecoveryError
    typ = event.get("type")
    if typ == "init":
        sid = event.get("session_id")
        try:
            uuid.UUID(str(sid))
        except ValueError as exc:
            raise RunRecoveryError("gemini_session_id_invalid") from exc
        if runner._resume_session_id and sid != runner._resume_session_id:
            raise RunRecoveryError("provider_resumed_a_different_session")
        runner._resume_session_id = sid
        if runner.recovery_enabled:
            runner._persist_run_manifest(run_state="running", provider_session_id=sid)
    if typ == "message" and event.get("role") == "assistant":
        runner.final_message_path.parent.mkdir(parents=True, exist_ok=True)
        with runner.final_message_path.open("a", encoding="utf-8") as handle:
            handle.write(str(event.get("content") or ""))
    if typ == "result":
        return {**event, "type": "turn.completed" if event.get("status") == "success" else "turn.failed"}
    return event


def refresh_usage(runner):
    """Account each native response once, including tool rounds and reasoning."""
    from .recovery import runner_store
    store = runner_store(runner)
    found = read_session(runner)
    if found:
        path, data = found
        key = "gemini:" + runner._resume_session_id
        total = {"input_tokens": 0, "output_tokens": 0, "cached_input_tokens": 0, "reasoning_output_tokens": 0}
        count = 0
        for msg in data.get("messages", []):
            if msg.get("type") != "gemini" or not msg.get("id"):
                continue
            count += 1
            tokens = msg.get("tokens") or {}
            values = {"input_tokens": tokens.get("input", 0),
                      "output_tokens": tokens.get("output", 0) + tokens.get("thoughts", 0),
                      "cached_input_tokens": tokens.get("cached", 0), "reasoning_output_tokens": tokens.get("thoughts", 0)}
            if any(type(n) is not int or n < 0 for n in values.values()):
                raise ValueError("Invalid Gemini native token counter")
            for name, n in values.items(): total[name] += n
            store.put_record("usage", key + ":" + msg["id"], {"session_id": runner._resume_session_id,
                             **values, "turns": 1, "reported_fields": values if tokens else {}})
        store.put_record("usage_stream", key, {"kind": "native", "session_id": runner._resume_session_id,
                         "segments": {"default": total}, "observable_model_steps": count,
                         "last_event_at": data.get("lastUpdated"), "source": str(path), "requests_without_identity": True})
    return store.usage_details()
