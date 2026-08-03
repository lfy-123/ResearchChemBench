from __future__ import annotations

import os
import re
from typing import Any
from urllib.parse import quote, urlsplit

import httpx

from src.assets.clues import normalize_doi, normalize_url
from src.core.io import stable_id

GITHUB_REPO = re.compile(r"^https?://github\.com/([^/]+)/([^/#?]+)", re.I)
ZENODO_RECORD = re.compile(r"zenodo\.org/(?:records?|record)/(\d+)", re.I)
ZENODO_DOI = re.compile(r"10\.5281/zenodo\.(\d+)", re.I)
OSF_NODE = re.compile(r"osf\.io/([a-z0-9]{5,})", re.I)
MATERIALS_CLOUD_DOI = re.compile(r"10\.24435/materialscloud:[^\s]+", re.I)
MATERIALS_CLOUD_RECORD = re.compile(r"archive\.materialscloud\.org/records/([^/?#]+)", re.I)


def metadata_clues(
    document: dict[str, Any], *, timeout_seconds: float = 30
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    doi = normalize_doi(document.get("doi"))
    if not doi:
        return [], []
    paper_id = str(document["paper_id"])
    endpoints = {
        "crossref": f"https://api.crossref.org/works/{quote(doi, safe='')}",
        "datacite": f"https://api.datacite.org/dois/{quote(doi, safe='')}",
        "openalex": f"https://api.openalex.org/works/https://doi.org/{doi}",
        "datacite_related": "https://api.datacite.org/dois",
    }
    clues: list[dict[str, Any]] = []
    audits: list[dict[str, Any]] = []
    with httpx.Client(timeout=timeout_seconds, follow_redirects=True) as client:
        for source, url in endpoints.items():
            audit = {"source": source, "url": url, "status": "failed", "error": None}
            try:
                params = None
                if source == "datacite_related":
                    params = {
                        "query": f'relatedIdentifiers.relatedIdentifier:"{doi}"',
                        "page[size]": 100,
                    }
                response = client.get(
                    url,
                    params=params,
                    headers={"User-Agent": "ResearchChemBench/1.0"},
                )
                response.raise_for_status()
                payload = response.json()
                audit["status"] = "success"
                clues.extend(_metadata_payload_clues(source, payload, paper_id, doi))
            except Exception as exc:
                audit["error"] = f"{type(exc).__name__}: {exc}"
            audits.append(audit)
    return clues, audits


def resolve_clue_targets(
    clue: dict[str, Any], *, timeout_seconds: float = 30
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    value = str(clue.get("canonical_value") or clue.get("value") or "")
    if not value:
        return [], []
    github = GITHUB_REPO.match(value)
    if github:
        return _github_targets(clue, github.group(1), github.group(2), timeout_seconds), []
    zenodo_id = _zenodo_id(value)
    if zenodo_id:
        return _zenodo_targets(clue, zenodo_id, timeout_seconds), []
    osf = OSF_NODE.search(value)
    if osf:
        return _osf_targets(clue, osf.group(1), timeout_seconds), []
    if MATERIALS_CLOUD_DOI.search(value) or MATERIALS_CLOUD_RECORD.search(value):
        return _materials_cloud_targets(clue, value, timeout_seconds), []
    if clue.get("kind") == "related_doi":
        return _datacite_targets(clue, value, timeout_seconds), []
    if clue.get("kind") in {"url", "repository_url"}:
        return [
            {
                "url": value,
                "role": _role_from_url(value),
                "relation_type": "explicit_url",
                "discovered_by": "document_link",
                "identifier": None,
                "version": None,
            }
        ], []
    return [], []


def _github_targets(
    clue: dict[str, Any], owner: str, repository: str, timeout: float
) -> list[dict[str, Any]]:
    repository = repository.removesuffix(".git")
    api = f"https://api.github.com/repos/{owner}/{repository}"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "ResearchChemBench/1.0"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with httpx.Client(timeout=timeout, follow_redirects=True, headers=headers) as client:
        response = client.get(api)
        response.raise_for_status()
        metadata = response.json()
    branch = metadata.get("default_branch") or "HEAD"
    return [
        {
            "url": f"https://api.github.com/repos/{owner}/{repository}/zipball/{branch}",
            "role": "code",
            "relation_type": "repository_match",
            "discovered_by": "github_api",
            "identifier": metadata.get("html_url") or clue.get("value"),
            "version": branch,
            "headers": headers,
            "file_name": f"{owner}-{repository}-{branch}.zip",
        }
    ]


def _zenodo_targets(clue: dict[str, Any], record_id: str, timeout: float) -> list[dict[str, Any]]:
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        response = client.get(f"https://zenodo.org/api/records/{record_id}")
        response.raise_for_status()
        record = response.json()
    targets = []
    for item in record.get("files", []):
        url = (item.get("links") or {}).get("self")
        if not url:
            continue
        targets.append(
            {
                "url": url,
                "role": "source_data",
                "relation_type": "related_identifier",
                "discovered_by": "zenodo_api",
                "identifier": record.get("doi") or clue.get("value"),
                "version": str(record.get("revision") or record.get("updated") or ""),
                "file_name": item.get("key"),
            }
        )
    return targets


def _osf_targets(clue: dict[str, Any], node_id: str, timeout: float) -> list[dict[str, Any]]:
    targets: list[dict[str, Any]] = []
    next_url: str | None = f"https://api.osf.io/v2/nodes/{node_id}/files/"
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        while next_url and len(targets) < 200:
            response = client.get(next_url)
            response.raise_for_status()
            payload = response.json()
            for provider in payload.get("data", []):
                files_url = (
                    (provider.get("relationships") or {})
                    .get("files", {})
                    .get("links", {})
                    .get("related", {})
                    .get("href")
                )
                if files_url:
                    targets.extend(
                        _osf_file_targets(client, files_url, clue, limit=200 - len(targets))
                    )
            next_url = (payload.get("links") or {}).get("next")
    return targets


def _osf_file_targets(
    client: httpx.Client, url: str, clue: dict[str, Any], *, limit: int
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    next_url: str | None = url
    while next_url and len(output) < limit:
        response = client.get(next_url)
        response.raise_for_status()
        payload = response.json()
        for item in payload.get("data", []):
            attributes = item.get("attributes") or {}
            links = item.get("links") or {}
            if attributes.get("kind") == "file" and links.get("download"):
                output.append(
                    {
                        "url": links["download"],
                        "role": "source_data",
                        "relation_type": "related_identifier",
                        "discovered_by": "osf_api",
                        "identifier": clue.get("value"),
                        "version": attributes.get("date_modified"),
                        "file_name": attributes.get("name"),
                    }
                )
        next_url = (payload.get("links") or {}).get("next")
    return output


def _materials_cloud_targets(
    clue: dict[str, Any], value: str, timeout: float
) -> list[dict[str, Any]]:
    landing = value
    doi = normalize_doi(value)
    if doi:
        landing = f"https://archive.materialscloud.org/doi/{doi}"
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        response = client.get(landing, headers={"User-Agent": "ResearchChemBench/1.0"})
        response.raise_for_status()
        match = MATERIALS_CLOUD_RECORD.search(str(response.url))
        if not match:
            raise RuntimeError(f"Materials Cloud record ID not found for {value}")
        record_id = match.group(1)
        record_response = client.get(f"https://archive.materialscloud.org/api/records/{record_id}")
        record_response.raise_for_status()
        record = record_response.json()
    version = str((record.get("metadata") or {}).get("version") or record.get("updated") or "")
    targets: list[dict[str, Any]] = []
    entries = ((record.get("files") or {}).get("entries") or {}).values()
    for item in entries:
        url = (item.get("links") or {}).get("content")
        if not url:
            continue
        targets.append(
            {
                "url": url,
                "role": "source_data",
                "relation_type": "related_identifier",
                "discovered_by": "materials_cloud_api",
                "identifier": doi or value,
                "version": version,
                "file_name": item.get("key"),
            }
        )
    return targets


def _datacite_targets(clue: dict[str, Any], doi: str, timeout: float) -> list[dict[str, Any]]:
    normalized = normalize_doi(doi)
    if not normalized:
        return []
    with httpx.Client(timeout=timeout, follow_redirects=True) as client:
        response = client.get(f"https://api.datacite.org/dois/{quote(normalized, safe='')}")
        if response.status_code == 404:
            return []
        response.raise_for_status()
        attributes = (response.json().get("data") or {}).get("attributes") or {}
    landing = str(attributes.get("url") or "")
    if MATERIALS_CLOUD_DOI.search(normalized) or MATERIALS_CLOUD_RECORD.search(landing):
        return _materials_cloud_targets(clue, landing or normalized, timeout)
    targets: list[dict[str, Any]] = []
    for url in attributes.get("contentUrl") or []:
        if isinstance(url, str) and url.startswith(("http://", "https://")):
            targets.append(
                {
                    "url": url,
                    "role": "source_data",
                    "relation_type": "related_identifier",
                    "discovered_by": "datacite",
                    "identifier": normalized,
                    "version": attributes.get("version"),
                }
            )
    if targets:
        return targets
    if landing and any(
        host in landing.casefold() for host in ("github.com", "zenodo.org", "osf.io")
    ):
        nested = dict(clue)
        nested["canonical_value"] = landing
        nested["value"] = landing
        nested["kind"] = "repository_url"
        return resolve_clue_targets(nested, timeout_seconds=timeout)[0]
    return []


def _zenodo_id(value: str) -> str | None:
    match = ZENODO_RECORD.search(value) or ZENODO_DOI.search(value)
    return match.group(1) if match else None


def _role_from_url(url: str) -> str:
    path = urlsplit(url).path.casefold()
    if path.endswith(".pdf"):
        return "supplement"
    if any(path.endswith(suffix) for suffix in (".zip", ".tar", ".gz", ".csv", ".json")):
        return "source_data"
    return "other"


def _metadata_payload_clues(
    source: str, payload: dict[str, Any], paper_id: str, paper_doi: str
) -> list[dict[str, Any]]:
    if source == "crossref":
        message = payload.get("message") or {}
        relations = message.get("relation") or {}
        output: list[dict[str, Any]] = []
        for relation_type, values in relations.items():
            if relation_type.casefold() not in {
                "has-data",
                "has-dataset",
                "has-component",
                "is-supplemented-by",
            }:
                continue
            for item in values or []:
                related = normalize_doi(item.get("id")) if isinstance(item, dict) else None
                if related and related != paper_doi:
                    output.append(
                        _derived_clue(
                            paper_id,
                            "related_doi",
                            related,
                            source,
                            f"Crossref relation {relation_type}",
                        )
                    )
        return output
    if source == "datacite_related":
        output = []
        for item in payload.get("data") or []:
            attributes = item.get("attributes") or {}
            types = attributes.get("types") or {}
            resource_type = str(types.get("resourceTypeGeneral") or "").casefold()
            version_doi = next(
                (
                    normalize_doi(relation.get("relatedIdentifier"))
                    for relation in attributes.get("relatedIdentifiers") or []
                    if relation.get("relationType") == "HasVersion"
                ),
                None,
            )
            related = version_doi or normalize_doi(item.get("id"))
            if not related or related == paper_doi or resource_type not in {"dataset", "software"}:
                continue
            clue = _derived_clue(
                paper_id,
                "related_doi",
                related,
                source,
                f"DataCite reverse relation ({resource_type}) to {paper_doi}",
            )
            clue["resource_type"] = resource_type
            output.append(clue)
        return output
    if source == "datacite":
        attributes = (payload.get("data") or {}).get("attributes") or {}
        return _datacite_attribute_clues(attributes, paper_id, source, paper_doi)
    return []


def _datacite_attribute_clues(
    attributes: dict[str, Any], paper_id: str, source: str, paper_doi: str
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for item in attributes.get("relatedIdentifiers") or []:
        relation = str(item.get("relationType") or "")
        related = normalize_doi(item.get("relatedIdentifier"))
        resource_type = str(item.get("resourceTypeGeneral") or "").casefold()
        if not related or related == paper_doi or resource_type not in {"dataset", "software"}:
            continue
        clue = _derived_clue(
            paper_id,
            "related_doi",
            related,
            source,
            f"DataCite relation {relation}",
        )
        clue["resource_type"] = resource_type
        output.append(clue)
    return output


def _derived_clue(
    paper_id: str, kind: str, value: str, source: str, evidence: str
) -> dict[str, Any]:
    canonical = normalize_url(value) if kind.endswith("url") else normalize_doi(value) or value
    return {
        "clue_id": stable_id("clue", paper_id, kind, str(canonical)),
        "paper_id": paper_id,
        "kind": kind,
        "value": value,
        "canonical_value": canonical,
        "discovery_round": 1,
        "source_asset_id": None,
        "evidence": evidence,
        "confidence": "high",
        "status": "pending",
        "discovered_by": source,
        "error": None,
    }
