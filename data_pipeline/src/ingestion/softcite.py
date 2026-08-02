from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.ingestion.managed_service import ManagedServiceError, managed_service


class SoftciteError(RuntimeError):
    pass


@dataclass(frozen=True)
class SoftciteClient:
    base_url: str = "http://127.0.0.1:8060"
    timeout_seconds: int = 300
    retries: int = 2

    def annotate_tei(self, tei_path: str | Path) -> dict[str, Any]:
        path = Path(tei_path).expanduser().resolve()
        boundary = f"----ResearchChemBench{uuid.uuid4().hex}"
        body = _multipart_file(boundary, path, {"disambiguate": "0", "addParagraphContext": "1"})
        return self._request_json(
            f"{self.base_url.rstrip('/')}/service/annotateSoftwareTEI",
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            empty_value={"mentions": []},
        )

    def characterize_context(self, text: str) -> dict[str, Any]:
        query = urllib.parse.urlencode({"text": text})
        return self._request_json(
            f"{self.base_url.rstrip('/')}/service/characterizeSoftwareContext?{query}",
            data=None,
            headers={},
        )

    def version(self) -> dict[str, Any]:
        return self._request_json(
            f"{self.base_url.rstrip('/')}/service/version", data=None, headers={}
        )

    def _request_json(
        self,
        url: str,
        *,
        data: bytes | None,
        headers: dict[str, str],
        empty_value: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        last_error: Exception | None = None
        for attempt in range(self.retries + 1):
            request = urllib.request.Request(url, data=data, headers=headers)
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    payload = response.read()
                    if response.status == 204:
                        return empty_value or {}
                    value = json.loads(payload.decode("utf-8", errors="replace"))
                    if not isinstance(value, dict):
                        raise SoftciteError("Softcite response must be a JSON object")
                    return value
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")[:2000]
                last_error = SoftciteError(
                    f"Softcite HTTP {exc.code}: {detail or exc.reason}"
                )
                if exc.code != 503 or attempt >= self.retries:
                    raise last_error from exc
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
                last_error = exc
                if attempt >= self.retries:
                    break
            time.sleep(min(8, 2**attempt))
        raise SoftciteError(f"Softcite request failed: {last_error}")


def softcite_service(config: dict[str, Any]):
    client = SoftciteClient(
        base_url=str(config.get("base_url", "http://127.0.0.1:8060")),
        timeout_seconds=int(config.get("timeout_seconds", 300)),
        retries=int(config.get("retries", 2)),
    )

    class _Context:
        def __enter__(self) -> SoftciteClient:
            try:
                self._manager = managed_service(config, service_name="Softcite")
                self._manager.__enter__()
            except ManagedServiceError as exc:
                raise SoftciteError(str(exc)) from exc
            client.version()
            return client

        def __exit__(self, exc_type, exc, traceback) -> bool:
            return bool(self._manager.__exit__(exc_type, exc, traceback))

    return _Context()


def _multipart_file(boundary: str, path: Path, fields: dict[str, str]) -> bytes:
    chunks: list[bytes] = []
    marker = boundary.encode("ascii")
    for name, value in fields.items():
        chunks.extend(
            [
                b"--" + marker + b"\r\n",
                f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode(),
                value.encode(),
                b"\r\n",
            ]
        )
    chunks.extend(
        [
            b"--" + marker + b"\r\n",
            f'Content-Disposition: form-data; name="input"; filename="{path.name}"\r\n'.encode(),
            b"Content-Type: application/xml\r\n\r\n",
            path.read_bytes(),
            b"\r\n--" + marker + b"--\r\n",
        ]
    )
    return b"".join(chunks)
