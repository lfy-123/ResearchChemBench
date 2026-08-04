from __future__ import annotations

import random
import threading
import time
from email.utils import parsedate_to_datetime
from typing import Any
from urllib.parse import urlsplit

import httpx

RETRYABLE_STATUS = {429, 500, 502, 503, 504}
_LOCK = threading.Lock()
_HOST_SEMAPHORES: dict[tuple[str, int], threading.BoundedSemaphore] = {}


def request_with_retry(
    client: httpx.Client,
    method: str,
    url: str,
    *,
    policy: dict[str, Any] | None = None,
    stream: bool = False,
    **kwargs: Any,
) -> httpx.Response:
    settings = policy or {}
    retries = max(0, int(settings.get("request_retries", 3)))
    base_delay = max(0.0, float(settings.get("retry_backoff_seconds", 1.0)))
    max_delay = max(base_delay, float(settings.get("retry_max_seconds", 60.0)))
    host = (urlsplit(url).hostname or "").casefold()
    semaphore = _host_semaphore(host, settings)
    last_error: Exception | None = None

    for attempt in range(retries + 1):
        try:
            with semaphore:
                request = client.build_request(method, url, **kwargs)
                response = client.send(request, stream=stream)
            if response.status_code not in RETRYABLE_STATUS or attempt >= retries:
                return response
            delay = _retry_delay(response, attempt, base_delay, max_delay)
            response.close()
        except (httpx.TimeoutException, httpx.NetworkError) as exc:
            last_error = exc
            if attempt >= retries:
                raise
            delay = min(max_delay, base_delay * (2**attempt))
        time.sleep(delay + random.uniform(0.0, min(0.25, delay / 4 if delay else 0.0)))

    if last_error:
        raise last_error
    raise RuntimeError(f"request failed without a response: {url}")


def _host_semaphore(host: str, policy: dict[str, Any]) -> threading.BoundedSemaphore:
    configured = policy.get("per_host_workers") or {}
    limit = max(1, int(configured.get(host, policy.get("default_per_host_workers", 2))))
    key = (host, limit)
    with _LOCK:
        return _HOST_SEMAPHORES.setdefault(key, threading.BoundedSemaphore(limit))


def _retry_delay(
    response: httpx.Response, attempt: int, base_delay: float, max_delay: float
) -> float:
    retry_after = response.headers.get("retry-after")
    if retry_after:
        try:
            return min(max_delay, max(0.0, float(retry_after)))
        except ValueError:
            try:
                value = parsedate_to_datetime(retry_after).timestamp() - time.time()
                return min(max_delay, max(0.0, value))
            except (TypeError, ValueError, OverflowError):
                pass
    reset = response.headers.get("x-ratelimit-reset")
    if reset:
        try:
            return min(max_delay, max(0.0, float(reset) - time.time()))
        except ValueError:
            pass
    return min(max_delay, base_delay * (2**attempt))
