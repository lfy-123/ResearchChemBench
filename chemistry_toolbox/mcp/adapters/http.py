"""Small bounded HTTP helpers used by public scientific-data tools."""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import Any


USER_AGENT = "ResearchChemBench/0.1 scientific-toolbox"


def get_json(
    url: str,
    *,
    query: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
    timeout_seconds: int = 30,
    max_bytes: int = 5_000_000,
) -> Any:
    if timeout_seconds <= 0 or max_bytes <= 0:
        raise ValueError("timeout_seconds and max_bytes must be positive")
    if query:
        separator = "&" if "?" in url else "?"
        url = url + separator + urllib.parse.urlencode(query)
    request_headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    request_headers.update(headers or {})
    request = urllib.request.Request(url, headers=request_headers)
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        payload = response.read(max_bytes + 1)
    if len(payload) > max_bytes:
        raise ValueError(f"HTTP response exceeded {max_bytes} bytes")
    return json.loads(payload.decode("utf-8"))


def post_json(
    url: str,
    payload: dict[str, Any],
    *,
    headers: dict[str, str] | None = None,
    timeout_seconds: int = 30,
    max_bytes: int = 5_000_000,
) -> Any:
    request_headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    request_headers.update(headers or {})
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=request_headers,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
        body = response.read(max_bytes + 1)
    if len(body) > max_bytes:
        raise ValueError(f"HTTP response exceeded {max_bytes} bytes")
    return json.loads(body.decode("utf-8"))

