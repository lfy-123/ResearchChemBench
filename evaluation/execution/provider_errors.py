"""Evidence-based provider failures shared by Agent and Judge; no retry side effects."""
from __future__ import annotations

import os
import json
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


def redact(value):
    text = str(value)
    for name, secret in os.environ.items():
        if any(word in name.upper() for word in ("KEY", "TOKEN", "SECRET", "PASSWORD")) and len(secret) >= 8:
            text = text.replace(secret, "[REDACTED]")
    text = re.sub(r"\b(?:sk-|agt_codex_)[A-Za-z0-9_-]+", "[REDACTED]", text)
    return re.sub(r"(?i)(bearer\s+)[\w.\-]+", r"\1[REDACTED]", text)


def is_encrypted_history_error(error):
    """Recognize the provider's replay error even inside a CLI stream wrapper."""
    if not isinstance(error, dict):
        return False
    if error.get("category") in {"quota", "authentication", "permission"}:
        return False
    if error.get("code") == "invalid_encrypted_content":
        return True
    message = str(error.get("message") or "").lower()
    return "invalid_encrypted_content" in message or bool(re.search(
        r"encrypted content(?: for item [\w-]+)? could not be verified", message)) or (
        "encrypted content could not be decrypted or parsed" in message)


def normalize_error(value, *, source, event_ref=None):
    body = value if isinstance(value, dict) else getattr(value, "body", None)
    body = body if isinstance(body, dict) else {}
    detail = body.get("error", body)
    detail = detail if isinstance(detail, dict) else {"message": str(detail)}
    # Codex/gateways sometimes place the original API error JSON in message.
    # Decode only a bounded error envelope; never guess fields from free text.
    for _ in range(3):
        embedded = detail.get("message")
        if not isinstance(embedded, str) or len(embedded) > 20000:
            break
        try:
            decoded = json.loads(embedded)
        except (ValueError, TypeError):
            break
        nested = decoded.get("error") if isinstance(decoded, dict) else None
        if not isinstance(nested, dict):
            break
        detail = {**detail, **nested}
    message = redact(detail.get("message") or str(value))[:2000]
    code = detail.get("code") or (detail.get("type") if detail is not body else None)
    status = body.get("status_code") or detail.get("status_code") or getattr(value, "status_code", None)
    response = getattr(value, "response", None)
    headers = body.get("headers") or getattr(response, "headers", {}) or {}
    headers = {str(k).lower(): v for k, v in headers.items()} if hasattr(headers, "items") else {}
    rules = (
        ("quota", ("insufficient_quota", "billing", "credit balance", "quota exceeded", "usage limit", "余额不足", "欠费")),
        ("authentication", ("invalid_api_key", "authentication", "unauthorized")),
        ("permission", ("permission_denied", "forbidden")),
        ("context_length", ("context_length_exceeded", "context window", "maximum context")),
        ("configuration", ("model_not_found", "unsupported_model", "invalid_request", "unsupported parameter", "invalid_encrypted_content")),
        ("rate_limit", ("rate_limit", "rate limit", "too many requests")),
        ("service_unavailable", ("server_error", "service_unavailable", "service unavailable", "overloaded", "bad gateway")),
        ("network", ("connection reset", "connection refused", "connection error", "stream disconnected", "timed out", "timeout", "network error")),
    )
    def classify(text, source):
        for name, markers in rules:
            found = next((marker for marker in markers if marker in text.lower()), None)
            if found:
                return name, source + ":" + found
        return "unknown_provider_failure", "unclassified"

    category, basis = classify(str(detail.get("code") or ""), "code")
    if category == "unknown_provider_failure":
        if status in (401, 403):
            category, basis = ("authentication" if status == 401 else "permission"), "http_status"
        elif isinstance(status, int) and 500 <= status < 600:
            category, basis = "service_unavailable", "http_status"
        else:
            category, basis = classify(message, "message")
            if category == "unknown_provider_failure":
                category, basis = classify(str(code or ""), "error_type")
    if category == "unknown_provider_failure" and (
            isinstance(value, (TimeoutError, ConnectionError)) or type(value).__name__ in {"APITimeoutError", "APIConnectionError"}):
        category, basis = "network", "exception_type"
    # The inner replay error is not a transient stream failure. Do not invent
    # an API error code when the gateway only returned human-readable text.
    if category not in {"quota", "authentication", "permission"} and is_encrypted_history_error({"code": code, "message": message}):
        category = "configuration"
        basis = "code:invalid_encrypted_content" if code == "invalid_encrypted_content" else "message:encrypted_history_rejected"
    result = {"category": category, "code": redact(code) if code else None, "message": message,
              "retryable": category in {"rate_limit", "service_unavailable", "network"},
              "source": source, "observed_at": datetime.now(timezone.utc).isoformat(),
              "event_ref": event_ref, "classification_basis": basis}
    if status is not None:
        result["http_status"] = status
    request_id = headers.get("x-request-id") or getattr(value, "request_id", None) or body.get("request_id")
    if request_id:
        result["request_id"] = redact(request_id)
    retry_after = headers.get("retry-after") or body.get("retry_after")
    if retry_after is not None:
        result["retry_after"] = redact(retry_after)
        try:
            result["retry_after_seconds"] = max(0, float(retry_after))
        except (ValueError, TypeError):
            try:
                result["retry_after_seconds"] = max(0, (parsedate_to_datetime(str(retry_after)) - datetime.now(timezone.utc)).total_seconds())
            except (ValueError, TypeError, OverflowError):
                pass
    return result


class ProviderFailure:
    """Warnings become failures only if the attempt actually fails."""
    def __init__(self):
        self.latest = None
        self.final = None
        self.count = 0
        self.first_ref = None

    def observe(self, event, ref):
        if event.get("type") not in {"error", "turn.failed"}:
            return
        error = normalize_error(event, source="agent", event_ref=ref)
        self.count += 1
        self.first_ref = self.first_ref or ref
        if error["category"] == "unknown_provider_failure" and self.latest:
            error = {**self.latest, "event_ref": ref}
        self.latest = error
        if event.get("type") == "turn.failed":
            self.final = error

    def failure(self, exit_code):
        return {**(self.final or self.latest or normalize_error(
            f"Provider exited with code {exit_code} without a successful final turn", source="agent")),
            "occurrences": self.count or 1, "first_event_ref": self.first_ref}
