from __future__ import annotations

import json
import os
import re
import tempfile
import time
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import urlparse

import httpx

from src.core.concurrency import ordered_parallel_map
from src.core.io import sha256_file
from src.core.logging import log_progress
from src.integrations.publishers import publisher_adapter


class ObjectStore(Protocol):
    def copy_to(self, uri: str, destination: str | Path) -> dict[str, Any]: ...


def acquire_supplementary_materials(
    papers: list[dict[str, Any]],
    output_dir: str | Path,
    config: dict[str, Any],
    *,
    store: ObjectStore | None = None,
    client: httpx.Client | None = None,
) -> list[dict[str, Any]]:
    root = Path(output_dir).expanduser().resolve()
    files_root = root / "files"
    files_root.mkdir(parents=True, exist_ok=True)
    own_client = client is None
    read_timeout = float(config.get("read_timeout_seconds", 20))
    connect_timeout = float(config.get("connect_timeout_seconds", 15))
    http = client or httpx.Client(
        timeout=httpx.Timeout(read_timeout, connect=connect_timeout),
        follow_redirects=True,
        headers={"User-Agent": "ResearchChemBench/1.0 supplementary-material collector"},
    )
    try:
        records = ordered_parallel_map(
            lambda paper: _acquire_one(
                paper, files_root, config, store=store, client=http
            ),
            papers,
            max_workers=int(config.get("workers", 1)),
            on_complete=lambda completed, total, _index, paper, record: log_progress(
                "stage_04_supplementary_acquisition",
                completed,
                total,
                str(paper["paper_id"]),
                status=record["supplementary_acquisition"]["download_status"],
            ),
        )
    finally:
        if own_client:
            http.close()
    return records


def supplementary_acquisition_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    statuses: dict[str, int] = {}
    attachments = 0
    for record in records:
        value = record.get("supplementary_acquisition") or {}
        status = str(value.get("download_status") or "unknown")
        statuses[status] = statuses.get(status, 0) + 1
        attachments += len(value.get("attachments") or [])
    return {"papers": len(records), "download_statuses": statuses, "attachments": attachments}


def _acquire_one(
    paper: dict[str, Any],
    files_root: Path,
    config: dict[str, Any],
    *,
    store: ObjectStore | None,
    client: httpx.Client,
) -> dict[str, Any]:
    deadline = time.monotonic() + float(config.get("paper_timeout_seconds", 180))
    paper_id = str(paper["paper_id"])
    if paper.get("has_local_supplementary") or paper.get("supplementary_documents"):
        return _result(
            paper,
            discovery_status="local_supplementary_found",
            download_status="skipped_existing_supplementary",
            attachments=[],
            attempts=[],
        )
    target_dir = files_root / paper_id
    target_dir.mkdir(parents=True, exist_ok=True)
    attempts: list[dict[str, Any]] = []
    remote_attachments = _copy_support_paths(paper, target_dir, store, attempts)
    if remote_attachments:
        return _result(
            paper,
            discovery_status="remote_paths_found",
            download_status="downloaded",
            attachments=remote_attachments,
            attempts=attempts,
        )
    if not config.get("enable_network", True):
        attempts.append({"source": "publisher", "status": "network_disabled"})
        return _result(
            paper,
            discovery_status="not_found",
            download_status="not_attempted",
            attachments=[],
            attempts=attempts,
        )
    adapter = publisher_adapter(
        doi=paper.get("doi"),
        article_url=paper.get("article_url"),
        enabled=config.get("publisher_adapters"),
    )
    if adapter is None:
        return _result(
            paper,
            discovery_status="not_found",
            download_status="not_attempted",
            attachments=[],
            attempts=attempts,
        )
    try:
        discovered, discovery = adapter.discover(
            client, doi=paper.get("doi"), article_url=paper.get("article_url")
        )
        attempts.append(discovery)
    except httpx.TimeoutException as exc:
        attempts.append({"source": "publisher", "status": "timeout", "error": str(exc)})
        return _result(paper, "metadata_error", "timeout", [], attempts)
    except httpx.HTTPStatusError as exc:
        status = "access_blocked" if exc.response.status_code in {401, 403, 429} else "metadata_error"
        attempts.append({"source": "publisher", "status": status, "http_status": exc.response.status_code})
        return _result(paper, "metadata_error", status, [], attempts)
    except Exception as exc:
        attempts.append({"source": "publisher", "status": "metadata_error", "error": f"{type(exc).__name__}: {exc}"})
        return _result(paper, "metadata_error", "not_attempted", [], attempts)
    if time.monotonic() >= deadline:
        attempts.append({"source": "publisher", "status": "paper_timeout"})
        return _result(paper, "metadata_error", "timeout", [], attempts)
    attachments, statuses = _download_official_attachments(
        discovered, adapter, target_dir, config, client, deadline=deadline
    )
    attempts.extend(statuses)
    if attachments and len(attachments) == len(discovered):
        status = "downloaded"
    elif attachments:
        status = "partial"
    elif any(item.get("status") == "access_blocked" for item in statuses):
        status = "access_blocked"
    elif any(item.get("status") in {"timeout", "paper_timeout"} for item in statuses):
        status = "timeout"
    elif any(item.get("status") == "oversize" for item in statuses):
        status = "oversize"
    else:
        status = "not_attempted" if not discovered else "unsupported_format"
    return _result(
        paper,
        "publisher_attachments_found" if discovered else "not_found",
        status,
        attachments,
        attempts,
    )


def _copy_support_paths(
    paper: dict[str, Any],
    target_dir: Path,
    store: ObjectStore | None,
    attempts: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    discovery = paper.get("supplementary_discovery") or {}
    paths = [
        str(value)
        for value in discovery.get("matched_remote_uris") or []
        if str(value).startswith("s3://")
    ]
    if not paths or store is None:
        return []
    attachments: list[dict[str, Any]] = []
    for index, uri in enumerate(paths, start=1):
        name = _safe_name(Path(uri).name or f"supplementary-{index}.pdf")
        destination = target_dir / name
        try:
            stat = store.copy_to(uri, destination)
        except Exception as exc:
            attempts.append({"source": "verified_remote_inventory", "url": uri, "status": "failed", "error": f"{type(exc).__name__}: {exc}"})
            continue
        attachment = _attachment_record(
            destination, uri, "verified_remote_inventory", stat
        )
        attachments.append(attachment)
        attempts.append(
            {"source": "verified_remote_inventory", "url": uri, "status": "downloaded"}
        )
    return attachments


def _download_official_attachments(
    discovered, adapter, target_dir, config, client, *, deadline
):
    allowed = {str(item).casefold().lstrip(".") for item in config.get("allowed_extensions", ["pdf"])}
    limit = int(config.get("max_attachments_per_paper", 20))
    max_file = int(config.get("max_file_bytes", 100 * 1024**2))
    max_total = int(config.get("max_total_bytes_per_paper", 250 * 1024**2))
    attachments: list[dict[str, Any]] = []
    attempts: list[dict[str, Any]] = []
    total = 0
    request_timeout = httpx.Timeout(
        float(config.get("read_timeout_seconds", 20)),
        connect=float(config.get("connect_timeout_seconds", 15)),
    )
    if len(discovered) > limit:
        attempts.append(
            {
                "source": "publisher",
                "status": "attachment_limit",
                "discovered": len(discovered),
                "attempted": limit,
            }
        )
    for item in discovered[:limit]:
        if time.monotonic() >= deadline:
            attempts.append({"source": "publisher", "status": "paper_timeout"})
            break
        if not adapter.official_attachment_url(item.url):
            attempts.append({"url": item.url, "status": "blocked_external_domain"})
            continue
        extension = Path(urlparse(item.url).path).suffix.casefold().lstrip(".")
        if extension and extension not in allowed:
            attempts.append({"url": item.url, "status": "unsupported_format"})
            continue
        name = _safe_name(item.file_name)
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{name}.", suffix=".part", dir=target_dir
        )
        os.close(descriptor)
        temporary = Path(temporary_name)
        path: Path | None = None
        size = 0
        content_type = ""
        rejected_status: str | None = None
        try:
            with client.stream("GET", item.url, timeout=request_timeout) as response:
                response.raise_for_status()
                content_type = response.headers.get("content-type", "").split(";", 1)[0].casefold()
                inferred = extension or ("pdf" if content_type == "application/pdf" else "")
                if inferred not in allowed:
                    rejected_status = "unsupported_format"
                declared_size = _content_length(response.headers.get("content-length"))
                if declared_size is not None and (
                    declared_size > max_file or total + declared_size > max_total
                ):
                    rejected_status = "oversize"
                if rejected_status is None:
                    with temporary.open("wb") as output:
                        for chunk in response.iter_bytes(chunk_size=1024 * 1024):
                            if time.monotonic() >= deadline:
                                rejected_status = "paper_timeout"
                                break
                            size += len(chunk)
                            if size > max_file or total + size > max_total:
                                rejected_status = "oversize"
                                break
                            output.write(chunk)
                        output.flush()
                        os.fsync(output.fileno())
                if rejected_status is None:
                    if not Path(name).suffix:
                        name += f".{inferred}"
                    path = _unique_path(target_dir / name)
                    os.replace(temporary, path)
        except httpx.HTTPStatusError as exc:
            status = "access_blocked" if exc.response.status_code in {401, 403, 429} else "download_error"
            attempts.append({"url": item.url, "status": status, "http_status": exc.response.status_code})
            continue
        except httpx.TimeoutException:
            attempts.append({"url": item.url, "status": "timeout"})
            continue
        finally:
            temporary.unlink(missing_ok=True)
        if rejected_status is not None:
            attempts.append(
                {
                    "url": item.url,
                    "status": rejected_status,
                    "size_bytes": size,
                    "content_type": content_type,
                }
            )
            if rejected_status == "paper_timeout":
                break
            continue
        assert path is not None
        total += size
        attachments.append(_attachment_record(path, item.url, f"publisher:{adapter.publisher}", {"size_bytes": size, "content_type": content_type}))
        attempts.append({"url": item.url, "status": "downloaded", "size_bytes": size})
    return attachments, attempts


def _content_length(value: str | None) -> int | None:
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _attachment_record(path: Path, url: str, source: str, stat: dict[str, Any]) -> dict[str, Any]:
    return {
        "source": source,
        "source_url": url,
        "path": str(path.resolve()),
        "file_name": path.name,
        "size_bytes": path.stat().st_size,
        "sha256": sha256_file(path),
        "etag": stat.get("etag"),
        "content_type": stat.get("content_type"),
        "document_role": "supplementary",
        "newly_downloaded": True,
    }


def _result(paper, discovery_status, download_status, attachments, attempts):
    return {
        **paper,
        "supplementary_acquisition": {
            "discovery_status": discovery_status,
            "download_status": download_status,
            "attachments": attachments,
            "attempts": attempts,
        },
        "pipeline_routing": {
            **(paper.get("pipeline_routing") or {}),
            "stage_04": download_status,
            "continue": True,
        },
    }


def _support_paths(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return [value]
        return [str(item) for item in parsed] if isinstance(parsed, list) else [value]
    return []


def _safe_name(value: str) -> str:
    return (re.sub(r"[^A-Za-z0-9._()-]+", "_", value).strip("._") or "supplementary.pdf")[:220]


def _unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    for index in range(2, 10_000):
        candidate = path.with_name(f"{path.stem}-{index}{path.suffix}")
        if not candidate.exists():
            return candidate
    raise RuntimeError(f"could not allocate attachment path below {path.parent}")
