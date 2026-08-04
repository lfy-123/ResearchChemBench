from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from src.core.io import stable_id

DOI_PATTERN = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)
URL_PATTERN = re.compile(r"https?://[^\s<>\"'{}|\\^`]+", re.I)
AVAILABILITY_TERMS = (
    "data availability",
    "code availability",
    "available at",
    "available from",
    "supporting information",
    "supplementary material",
    "source data",
    "repository",
    "dataset",
)
REPOSITORY_HOSTS = (
    "github.com",
    "gitlab.com",
    "bitbucket.org",
    "zenodo.org",
    "osf.io",
    "figshare.com",
    "dataverse",
    "nomad-lab.eu",
    "materialscloud.org",
)
TRACKING_KEYS = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"}


def seed_document_clues(document: dict[str, Any], *, max_clues: int = 200) -> list[dict[str, Any]]:
    text_parts = [str(document.get("abstract") or "")]
    for key in ("text_path", "grobid_text_path"):
        path = Path(str(document.get(key) or ""))
        if path.is_file():
            text_parts.append(path.read_text(encoding="utf-8", errors="replace"))
    clues = extract_clues(
        "\n".join(text_parts),
        paper_id=str(document["paper_id"]),
        discovery_round=1,
        source_asset_id=None,
        max_clues=max_clues,
    )
    tei_path = Path(str(document.get("grobid_tei_path") or ""))
    if tei_path.is_file():
        clues.extend(_tei_availability_clues(tei_path, str(document["paper_id"]), max_clues))
    doi = normalize_doi(document.get("doi"))
    if doi:
        clues = [
            item
            for item in clues
            if not (item.get("kind") == "related_doi" and item.get("canonical_value") == doi)
        ]
        paper_doi = _clue(
            paper_id=str(document["paper_id"]),
            kind="paper_doi",
            value=doi,
            discovery_round=1,
            source_asset_id=None,
            evidence=f"GROBID DOI: {doi}",
            confidence="high",
        )
        paper_doi["status"] = "resolved"
        paper_doi["resolution"] = "paper_identity"
        clues.insert(0, paper_doi)
    return deduplicate_clues(clues)[:max_clues]


def extract_clues(
    text: str,
    *,
    paper_id: str,
    discovery_round: int,
    source_asset_id: str | None,
    max_clues: int = 200,
) -> list[dict[str, Any]]:
    clues: list[dict[str, Any]] = []
    for match in URL_PATTERN.finditer(text):
        raw = match.group(0).rstrip(".,;:)]}")
        value = normalize_url(raw)
        if not value:
            continue
        context = _context(text, match.start(), match.end())
        host = urlsplit(value).hostname or ""
        if _is_non_asset_page(value):
            continue
        availability = any(term in context.casefold() for term in AVAILABILITY_TERMS)
        repository = any(term in host.casefold() for term in REPOSITORY_HOSTS)
        if not (availability or repository or _looks_like_asset_url(value)):
            continue
        clues.append(
            _clue(
                paper_id=paper_id,
                kind="repository_url" if repository else "url",
                value=value,
                discovery_round=discovery_round,
                source_asset_id=source_asset_id,
                evidence=context,
                confidence="high" if availability else "medium",
            )
        )
    for match in DOI_PATTERN.finditer(text):
        doi = normalize_doi(match.group(0))
        context = _context(text, match.start(), match.end())
        if not doi or not any(term in context.casefold() for term in AVAILABILITY_TERMS):
            continue
        clues.append(
            _clue(
                paper_id=paper_id,
                kind="related_doi",
                value=doi,
                discovery_round=discovery_round,
                source_asset_id=source_asset_id,
                evidence=context,
                confidence="high",
            )
        )
    return deduplicate_clues(clues)[:max_clues]


def deduplicate_clues(clues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for clue in clues:
        key = (str(clue.get("kind")), str(clue.get("canonical_value")))
        if key in seen:
            continue
        seen.add(key)
        output.append(clue)
    return output


def normalize_url(value: Any) -> str | None:
    if not value:
        return None
    raw = str(value).strip().rstrip(".,;:)]}")
    try:
        parts = urlsplit(raw)
    except ValueError:
        return None
    if (
        parts.scheme.casefold() not in {"http", "https"}
        or not parts.hostname
        or "." not in parts.hostname
    ):
        return None
    if parts.path.endswith("-"):
        return None
    query = urlencode(
        [
            (key, item)
            for key, item in parse_qsl(parts.query, keep_blank_values=True)
            if key not in TRACKING_KEYS
        ]
    )
    return urlunsplit((parts.scheme.casefold(), parts.netloc.casefold(), parts.path, query, ""))


def normalize_doi(value: Any) -> str | None:
    if not value:
        return None
    raw = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", str(value).strip(), flags=re.I)
    match = DOI_PATTERN.search(raw)
    return match.group(0).rstrip(".,;:)]}").casefold() if match else None


def _clue(
    *,
    paper_id: str,
    kind: str,
    value: str,
    discovery_round: int,
    source_asset_id: str | None,
    evidence: str,
    confidence: str,
) -> dict[str, Any]:
    canonical = normalize_url(value) if kind.endswith("url") else normalize_doi(value) or value
    return {
        "clue_id": stable_id("clue", paper_id, kind, str(canonical)),
        "paper_id": paper_id,
        "kind": kind,
        "value": value,
        "canonical_value": canonical,
        "discovery_round": discovery_round,
        "source_asset_id": source_asset_id,
        "evidence": " ".join(evidence.split())[:1000],
        "confidence": confidence,
        "status": "pending",
        "error": None,
    }


def _context(text: str, start: int, end: int, radius: int = 240) -> str:
    lower = max(0, start - radius)
    upper = min(len(text), end + radius)
    sentence_start = max(text.rfind(". ", lower, start), text.rfind("\n", lower, start))
    sentence_end_candidates = [
        value for value in (text.find(". ", end, upper), text.find("\n", end, upper)) if value >= 0
    ]
    sentence_end = min(sentence_end_candidates) + 1 if sentence_end_candidates else upper
    return " ".join(text[sentence_start + 1 : sentence_end].split())


def _looks_like_asset_url(url: str) -> bool:
    path = urlsplit(url).path.casefold()
    return any(
        path.endswith(suffix)
        for suffix in (
            ".zip",
            ".tar",
            ".tar.gz",
            ".tgz",
            ".pdf",
            ".csv",
            ".tsv",
            ".xlsx",
            ".json",
            ".yaml",
            ".yml",
            ".xyz",
            ".cif",
            ".pdb",
            ".gro",
            ".mol",
            ".sdf",
        )
    )


def _is_non_asset_page(url: str) -> bool:
    parts = urlsplit(url)
    host = (parts.hostname or "").casefold()
    path = parts.path.rstrip("/").casefold()
    if host in {"www.tei-c.org", "tei-c.org", "openalex.org", "orcid.org", "ror.org"}:
        return True
    if host.endswith(".readthedocs.io") or path == "/download":
        return True
    return host in {"nature.com", "www.nature.com"} and not path


def _tei_availability_clues(path: Path, paper_id: str, max_clues: int) -> list[dict[str, Any]]:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return []
    output: list[dict[str, Any]] = []
    section_terms = (
        "data availability",
        "code availability",
        "availability of data",
        "availability of code",
        "supplementary information",
        "supporting information",
    )
    for element in root.iter():
        if _local_name(element.tag) != "div":
            continue
        heading = next(
            (
                " ".join("".join(child.itertext()).split()).casefold()
                for child in element
                if _local_name(child.tag) == "head"
            ),
            "",
        )
        if not any(term in heading for term in section_terms):
            continue
        targets = [
            str(child.get("target"))
            for child in element.iter()
            if child.get("target", "").startswith(("http://", "https://"))
        ]
        section = " ".join([" ".join(element.itertext()), *targets])
        section_clues = extract_clues(
            section,
            paper_id=paper_id,
            discovery_round=1,
            source_asset_id=None,
            max_clues=max_clues,
        )
        if "code availability" in heading or "availability of code" in heading:
            section_clues = [
                item
                for item in section_clues
                if item.get("kind") == "repository_url"
                or _looks_like_asset_url(str(item.get("canonical_value") or ""))
            ]
        output.extend(section_clues)
    return deduplicate_clues(output)[:max_clues]


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]
