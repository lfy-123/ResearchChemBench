"""Claude Code native session persistence and exact-session recovery."""
from __future__ import annotations

import json
import uuid
from pathlib import Path


def context_environment(window, threshold, env):
    """Map an absolute token threshold to Claude Code 2.1.312's native controls."""
    # The CLI reserves at most 20k output tokens and another 13k for compaction.
    effective_window = window - min(int(env.get("CLAUDE_CODE_MAX_OUTPUT_TOKENS", "32000")), 20000)
    if not 100000 <= window <= 1000000 or not 0 < threshold <= effective_window - 13000:
        raise ValueError("Claude requires a 100000–1000000 context window and a compression threshold leaving output/compaction headroom")
    return {
        "CLAUDE_CODE_MAX_CONTEXT_TOKENS": str(window),
        "CLAUDE_CODE_AUTO_COMPACT_WINDOW": str(window),
        # +0.5 keeps the CLI's floor() at the requested integer after rounding.
        "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE": str(100 * (threshold + 0.5) / effective_window),
    }


def session_home(runner):
    from .recovery import runner_store
    return runner_store(runner).directory / "claude"


def prepare(runner, env):
    from .recovery import RunRecoveryError, runner_store
    provider = {"model": runner.agent.get("model", ""),
                **{k: env.get(k, "") for k in ("ANTHROPIC_BASE_URL", "ANTHROPIC_DEFAULT_OPUS_MODEL",
                    "ANTHROPIC_DEFAULT_SONNET_MODEL", "ANTHROPIC_DEFAULT_HAIKU_MODEL")}}
    store = runner_store(runner)
    saved = store.get_record("claude", "provider")
    if saved is not None and saved != provider:
        raise RunRecoveryError("claude_provider_configuration_drift")
    store.put_record("claude", "provider", provider, immutable=True)
    home = session_home(runner)
    home.mkdir(parents=True, exist_ok=True, mode=0o700)
    env.update(CLAUDE_CONFIG_DIR=str(home), DISABLE_AUTOUPDATER="1")
    return env


def session_path(runner, *, required=False):
    from .recovery import RunRecoveryError
    sid = runner._resume_session_id
    try:
        uuid.UUID(str(sid))
    except ValueError as exc:
        if required:
            raise RunRecoveryError("claude_session_id_invalid") from exc
        return None
    home = session_home(runner).resolve()
    matches = list((home / "projects").glob("*/" + sid + ".jsonl"))
    if len(matches) != 1:
        if required:
            raise RunRecoveryError("claude_session_missing_or_ambiguous; original run must save native sessions")
        return None
    path = matches[0]
    if not path.resolve().is_relative_to(home):
        raise RunRecoveryError("claude_session_path_invalid")
    if required:
        found = False
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                if not line.endswith("\n"):
                    break  # An interrupted final append is not a saved message.
                event = json.loads(line)
                if event.get("type") not in {"user", "assistant"}:
                    continue
                if event.get("sessionId") != sid or not Path(event.get("cwd", "")).resolve().is_relative_to(runner.workspace.resolve()):
                    raise RunRecoveryError("claude_session_workspace_or_identity_mismatch")
                found = True
        if not found:
            raise RunRecoveryError("claude_session_has_no_messages")
    return path


def capture(runner, event):
    from .recovery import RunRecoveryError
    if event.get("type") == "system" and event.get("subtype") == "init":
        sid = event.get("session_id")
        try:
            uuid.UUID(str(sid))
        except ValueError as exc:
            raise RunRecoveryError("claude_session_id_invalid") from exc
        if runner._resume_session_id and sid != runner._resume_session_id:
            raise RunRecoveryError("provider_resumed_a_different_session")
        runner._resume_session_id = sid
        if runner.recovery_enabled:
            runner._persist_run_manifest(run_state="running", provider_session_id=sid)
    if event.get("type") == "result":
        success = event.get("subtype") == "success" and not event.get("is_error")
        if success:
            runner.final_message_path.parent.mkdir(parents=True, exist_ok=True)
            runner.final_message_path.write_text(str(event.get("result") or ""), encoding="utf-8")
        return {**event, "type": "turn.completed" if success else "turn.failed",
                "error": None if success else {"code": None if event.get("subtype") == "success" else event.get("subtype"),
                    "message": "\n".join(event.get("errors") or [str(event.get("result") or event.get("subtype"))]),
                    "status_code": event.get("api_error_status")}}
    return event


def refresh_usage(runner, *, force=False):
    from .recovery import runner_store
    from .usage_accounting import ingest_file
    store = runner_store(runner)
    path = session_path(runner)
    if path:
        for _ in range(8 if force else 1):
            value = ingest_file(store, path, session_id=runner._resume_session_id, kind="claude")
            if value.get("backlog_bytes", 0) < 2 * 1024 * 1024:
                break
    return store.usage_details()
