from __future__ import annotations

import ipaddress
import os
import shutil
import socket
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit

import httpx

from src.core.io import sha256_file, stable_id


class DownloadError(RuntimeError):
    pass


TRUSTED_HTTPS_HOSTS = {
    "api.github.com",
    "codeload.github.com",
    "github.com",
    "github-releases.githubusercontent.com",
    "objects.githubusercontent.com",
    "raw.githubusercontent.com",
}


def register_local_file(
    path: str | Path,
    *,
    paper_id: str,
    object_root: Path,
    role: str,
    relation_type: str,
    discovered_by: str,
    discovery_round: int,
    parent_asset_id: str | None = None,
    archive_depth: int = 0,
    fallback_text_path: str | None = None,
) -> dict[str, Any]:
    source = Path(path).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    digest = sha256_file(source)
    target = object_root / digest[:2] / digest
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        try:
            os.link(source, target)
        except OSError:
            shutil.copy2(source, target)
    return {
        "schema_version": "1.0",
        "asset_id": stable_id("asset", digest, length=16),
        "paper_id": paper_id,
        "parent_asset_id": parent_asset_id,
        "discovery_round": discovery_round,
        "archive_depth": archive_depth,
        "role": role,
        "relation_type": relation_type,
        "discovered_by": discovered_by,
        "evidence": str(source),
        "confidence": "high",
        "source_url": None,
        "resolved_url": None,
        "identifier": None,
        "version": None,
        "license": "unknown",
        "access_status": "downloaded",
        "sha256": digest,
        "size_bytes": source.stat().st_size,
        "media_type": _guess_media_type(source.name),
        "file_name": source.name,
        "original_path": str(target.resolve()),
        "source_local_path": str(source),
        "fallback_text_path": fallback_text_path,
        "parser": None,
        "parse_status": "pending",
        "structured_path": None,
        "readable_paths": [],
        "error": None,
    }


def download_url(
    url: str,
    *,
    paper_id: str,
    object_root: Path,
    role: str,
    relation_type: str,
    discovered_by: str,
    discovery_round: int,
    parent_asset_id: str | None = None,
    archive_depth: int = 0,
    timeout_seconds: float = 60,
    max_bytes: int = 10 * 1024**3,
    headers: dict[str, str] | None = None,
) -> dict[str, Any]:
    current = url
    history: list[str] = []
    request_headers = {"User-Agent": "ResearchChemBench-asset-collector/1.0", **(headers or {})}
    object_root.mkdir(parents=True, exist_ok=True)
    with httpx.Client(
        timeout=timeout_seconds, follow_redirects=False, headers=request_headers
    ) as client:
        response: httpx.Response | None = None
        for _ in range(6):
            validate_public_url(current)
            response = client.send(client.build_request("GET", current), stream=True)
            history.append(redact_url(current))
            if response.status_code in {301, 302, 303, 307, 308}:
                location = response.headers.get("location")
                response.close()
                if not location:
                    raise DownloadError(f"redirect without location: {redact_url(current)}")
                current = urljoin(current, location)
                continue
            break
        if response is None or response.status_code in {301, 302, 303, 307, 308}:
            if response is not None:
                response.close()
            raise DownloadError(f"too many redirects: {redact_url(url)}")
        try:
            response.raise_for_status()
            length = int(response.headers.get("content-length") or 0)
            if length and length > max_bytes:
                raise DownloadError(f"content length {length} exceeds limit {max_bytes}")
            fd, temporary = tempfile.mkstemp(prefix="download-", dir=object_root)
            size = 0
            try:
                with os.fdopen(fd, "wb") as handle:
                    for chunk in response.iter_bytes(1024 * 1024):
                        size += len(chunk)
                        if size > max_bytes:
                            raise DownloadError(f"download exceeds limit {max_bytes}")
                        handle.write(chunk)
                digest = sha256_file(temporary)
                target = object_root / digest[:2] / digest
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists():
                    Path(temporary).unlink()
                else:
                    os.replace(temporary, target)
            except Exception:
                Path(temporary).unlink(missing_ok=True)
                raise
        finally:
            response.close()
    file_name = _response_filename(response, current)
    return {
        "schema_version": "1.0",
        "asset_id": stable_id("asset", digest, length=16),
        "paper_id": paper_id,
        "parent_asset_id": parent_asset_id,
        "discovery_round": discovery_round,
        "archive_depth": archive_depth,
        "role": role,
        "relation_type": relation_type,
        "discovered_by": discovered_by,
        "evidence": history,
        "confidence": "high"
        if relation_type in {"explicit_url", "publisher_attachment"}
        else "medium",
        "source_url": redact_url(url),
        "resolved_url": redact_url(current),
        "identifier": None,
        "version": response.headers.get("etag") or response.headers.get("last-modified"),
        "license": "unknown",
        "access_status": "downloaded",
        "sha256": digest,
        "size_bytes": size,
        "media_type": response.headers.get("content-type", "").split(";", 1)[0]
        or _guess_media_type(file_name),
        "file_name": file_name,
        "original_path": str(target.resolve()),
        "source_local_path": None,
        "fallback_text_path": None,
        "parser": None,
        "parse_status": "pending",
        "structured_path": None,
        "readable_paths": [],
        "error": None,
    }


def validate_public_url(url: str) -> None:
    parts = urlsplit(url)
    if parts.scheme.casefold() not in {"http", "https"} or not parts.hostname:
        raise DownloadError("only public HTTP(S) URLs are allowed")
    host = parts.hostname.casefold()
    if host in {"localhost", "localhost.localdomain"}:
        raise DownloadError("localhost URLs are not allowed")
    if parts.scheme.casefold() == "https" and host in TRUSTED_HTTPS_HOSTS:
        return
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(host, parts.port or 443)}
    except socket.gaierror as exc:
        raise DownloadError(f"DNS resolution failed for {host}: {exc}") from exc
    for value in addresses:
        address = ipaddress.ip_address(value)
        if not address.is_global:
            raise DownloadError(f"non-public address is not allowed: {address}")


def redact_url(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def _response_filename(response: httpx.Response, url: str) -> str:
    disposition = response.headers.get("content-disposition", "")
    if "filename=" in disposition:
        value = disposition.split("filename=", 1)[1].strip().strip('"')
        if value:
            return Path(unquote(value)).name
    name = Path(unquote(urlsplit(url).path)).name
    return name or "downloaded_asset"


def _guess_media_type(name: str) -> str:
    suffix = name.casefold()
    mapping = {
        ".pdf": "application/pdf",
        ".zip": "application/zip",
        ".json": "application/json",
        ".csv": "text/csv",
        ".txt": "text/plain",
        ".md": "text/markdown",
        ".xml": "application/xml",
        ".html": "text/html",
    }
    return next(
        (value for key, value in mapping.items() if suffix.endswith(key)),
        "application/octet-stream",
    )
