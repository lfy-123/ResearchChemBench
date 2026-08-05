from __future__ import annotations

import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from typing import Any

from src.integrations.managed_service import ManagedServiceError, managed_service


class GrobidQuantitiesError(RuntimeError):
    pass


@dataclass(frozen=True)
class GrobidQuantitiesClient:
    base_url: str = "http://127.0.0.1:8062"
    timeout_seconds: int = 120
    retries: int = 2

    def process_text(self, text: str) -> dict[str, Any]:
        boundary = f"----ResearchChemBench{uuid.uuid4().hex}"
        body = _multipart_text(boundary, "text", text)
        return self._request_json(
            f"{self.base_url.rstrip('/')}/service/processQuantityText",
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )

    def version(self) -> dict[str, Any]:
        return self._request_json(
            f"{self.base_url.rstrip('/')}/service/version", data=None, headers={}
        )

    def _request_json(
        self, url: str, *, data: bytes | None, headers: dict[str, str]
    ) -> dict[str, Any]:
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            request = urllib.request.Request(url, data=data, headers=headers)
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    value = json.load(response)
                if not isinstance(value, dict):
                    raise GrobidQuantitiesError("GROBID Quantities response must be an object")
                return value
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")[:2000]
                last_error = GrobidQuantitiesError(
                    f"GROBID Quantities HTTP {exc.code}: {detail or exc.reason}"
                )
                if exc.code != 503 or attempt >= self.retries:
                    raise last_error from exc
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                last_error = exc
                if attempt >= self.retries:
                    break
            time.sleep(min(8, 2**attempt))
        raise GrobidQuantitiesError(f"GROBID Quantities request failed: {last_error}")


def grobid_quantities_service(config: dict[str, Any]):
    client = GrobidQuantitiesClient(
        base_url=str(config.get("base_url", "http://127.0.0.1:8062")),
        timeout_seconds=int(config.get("timeout_seconds", 120)),
        retries=int(config.get("retries", 2)),
    )

    class _Context:
        def __enter__(self) -> GrobidQuantitiesClient:
            try:
                self._manager = managed_service(
                    config,
                    service_name="GROBID Quantities",
                    sandbox_service="quantities",
                )
                self._manager.__enter__()
            except ManagedServiceError as exc:
                raise GrobidQuantitiesError(str(exc)) from exc
            try:
                client.version()
            except Exception:
                self._manager.__exit__(*sys.exc_info())
                raise
            return client

        def __exit__(self, exc_type, exc, traceback) -> bool:
            return bool(self._manager.__exit__(exc_type, exc, traceback))

    return _Context()


def _multipart_text(boundary: str, field_name: str, value: str) -> bytes:
    return (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field_name}"\r\n\r\n'
        f"{value}\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")
