from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Any

_CREDENTIAL_RE = re.compile(r"^(AK|SK)\s*[:：]\s*(.+)$", re.IGNORECASE)


def read_xinghe_access(
    path: str | Path,
) -> tuple[str, str, str, str | None, tuple[str, ...]]:
    source = Path(path).expanduser().resolve()
    if not source.is_file():
        raise ValueError(f"Xinghe credential file not found: {source}")
    values: dict[str, str] = {}
    endpoints: list[str] = []
    prefixes: list[str] = []
    for raw in source.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        match = _CREDENTIAL_RE.match(line)
        if match:
            values[match.group(1).upper()] = match.group(2).strip()
        elif line.startswith(("http://", "https://")):
            endpoints.append(line.rstrip("/"))
        elif line.startswith("s3://"):
            prefixes.append(line.rstrip("/") + "/")
    if not values.get("AK") or not values.get("SK"):
        raise ValueError(f"{source} must contain AK and SK")
    if not endpoints or not prefixes:
        raise ValueError(f"{source} must contain an endpoint and authorized prefixes")
    inside = next((item for item in endpoints if "inside" in item), endpoints[0])
    outside = next((item for item in endpoints if "outside" in item), None)
    return values["AK"], values["SK"], inside, outside, tuple(dict.fromkeys(prefixes))


def validate_authorized_uri(uri: str, prefixes: tuple[str, ...]) -> str:
    value = str(uri).strip()
    if not value.startswith("s3://"):
        raise ValueError(f"remote URI must use s3://: {value}")
    if not any(value == prefix.rstrip("/") or value.startswith(prefix) for prefix in prefixes):
        raise PermissionError(f"remote URI is outside authorized prefixes: {value}")
    return value


def split_s3_uri(uri: str) -> tuple[str, str]:
    value = uri.removeprefix("s3://")
    bucket, separator, key = value.partition("/")
    if not separator or not bucket or not key:
        raise ValueError(f"invalid S3 URI: {uri}")
    return bucket, key


class XingheObjectStore:
    """Small read-only object-store adapter used by Stage 00 and Stage 04."""

    def __init__(self, credential_file: str | Path, *, outside: bool = False):
        try:
            import boto3
            from botocore.config import Config
        except ImportError as exc:  # pragma: no cover - environment contract
            raise RuntimeError("boto3 is required for Xinghe access") from exc
        access, secret, inside, outside_endpoint, prefixes = read_xinghe_access(credential_file)
        endpoint = outside_endpoint if outside else inside
        if not endpoint:
            raise ValueError("outside endpoint is not configured")
        self.prefixes = prefixes
        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint,
            aws_access_key_id=access,
            aws_secret_access_key=secret,
            config=Config(
                connect_timeout=10,
                read_timeout=300,
                retries={"max_attempts": 5, "mode": "standard"},
                s3={"addressing_style": "path"},
            ),
        )

    def iter_uris(self, prefix: str, *, start_after: str | None = None) -> Iterator[str]:
        target = validate_authorized_uri(prefix.rstrip("/") + "/", self.prefixes)
        bucket, key_prefix = split_s3_uri(target)
        pagination: dict[str, Any] = {"PageSize": 1000}
        request: dict[str, Any] = {"Bucket": bucket, "Prefix": key_prefix}
        if start_after:
            _, start_key = split_s3_uri(validate_authorized_uri(start_after, self.prefixes))
            request["StartAfter"] = start_key
        paginator = self.client.get_paginator("list_objects_v2")
        for page in paginator.paginate(
            **request,
            PaginationConfig={key: value for key, value in pagination.items() if value is not None},
        ):
            for item in page.get("Contents", ()):
                key = str(item["Key"])
                uri = f"s3://{bucket}/{key}"
                if start_after and uri <= start_after:
                    continue
                yield uri

    def iter_jsonl(self, uri: str) -> Iterator[dict[str, Any]]:
        bucket, key = split_s3_uri(validate_authorized_uri(uri, self.prefixes))
        body = self.client.get_object(Bucket=bucket, Key=key)["Body"]
        try:
            for raw in body.iter_lines(chunk_size=1024 * 1024):
                if not raw:
                    continue
                try:
                    value = json.loads(raw)
                except (UnicodeDecodeError, json.JSONDecodeError):
                    continue
                if isinstance(value, dict):
                    yield value
        finally:
            body.close()

    def stat(self, uri: str) -> dict[str, Any]:
        bucket, key = split_s3_uri(validate_authorized_uri(uri, self.prefixes))
        value = self.client.head_object(Bucket=bucket, Key=key)
        return {
            "size_bytes": int(value.get("ContentLength") or 0),
            "etag": str(value.get("ETag") or "").strip('"') or None,
            "content_type": value.get("ContentType"),
        }

    def copy_to(self, uri: str, destination: str | Path) -> dict[str, Any]:
        bucket, key = split_s3_uri(validate_authorized_uri(uri, self.prefixes))
        target = Path(destination)
        target.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{target.name}.", dir=target.parent)
        os.close(descriptor)
        temporary = Path(temporary_name)
        response = None
        try:
            response = self.client.get_object(Bucket=bucket, Key=key)
            with temporary.open("wb") as output:
                shutil.copyfileobj(response["Body"], output, length=1024 * 1024)
                output.flush()
                os.fsync(output.fileno())
            os.replace(temporary, target)
        except Exception:
            temporary.unlink(missing_ok=True)
            raise
        finally:
            if response is not None:
                response["Body"].close()
        return self.stat(uri)
