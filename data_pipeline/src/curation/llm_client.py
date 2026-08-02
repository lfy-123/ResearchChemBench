from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any

from json_repair import repair_json


def call_json_chat(
    *,
    model: str,
    base_url: str,
    api_key: str,
    system_prompt: str,
    user_content: str,
    timeout_seconds: float = 600,
    max_tokens: int | None = None,
    retries: int = 2,
    thinking: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Call an OpenAI-compatible chat endpoint and return parsed JSON plus audit metadata."""

    payload: dict[str, Any] = {
        "model": model,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
    }
    if max_tokens:
        payload["max_tokens"] = int(max_tokens)
    if thinking:
        payload["thinking"] = {"type": thinking}

    last_error: Exception | None = None
    for attempt in range(retries + 1):
        request = urllib.request.Request(
            f"{base_url.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
        )
        started = time.monotonic()
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                result = json.load(response)
                request_id = response.headers.get("x-request-id")
            choice = result["choices"][0]
            content = (choice.get("message") or {}).get("content") or ""
            value = _parse_json_object(content)
            return value, {
                "provider": "openai_compatible",
                "model_requested": model,
                "model_returned": result.get("model"),
                "request_id": request_id,
                "finish_reason": choice.get("finish_reason"),
                "usage": result.get("usage", {}),
                "duration_seconds": round(time.monotonic() - started, 3),
                "attempts": attempt + 1,
                "thinking": thinking or "provider_default",
            }
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:2000]
            last_error = RuntimeError(f"LLM HTTP {exc.code}: {body}")
            if exc.code not in {408, 409, 429, 500, 502, 503, 504} or attempt >= retries:
                raise last_error from exc
        except (
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError,
            urllib.error.URLError,
        ) as exc:
            last_error = exc
            if attempt >= retries:
                raise
        time.sleep(min(2**attempt, 8))
    raise RuntimeError(f"LLM call failed: {last_error}")


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
        candidate = cleaned[start : end + 1]
        try:
            value = json.loads(candidate)
        except json.JSONDecodeError:
            value = repair_json(candidate, return_objects=True)
    if not isinstance(value, dict):
        raise ValueError("LLM response must be one JSON object")
    return value
