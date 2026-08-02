from __future__ import annotations

import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from src.core.models import TASK_TYPES, task_types_for_record

URL_PATTERN = re.compile(r"https?://[^\s<>()\[\]{}\"']+", re.I)
DOI_PATTERN = re.compile(r"(?<![\w/])(10\.\d{4,9}/[-._;()/:A-Z0-9]+)", re.I)
PDB_PATTERN = re.compile(r"\bPDB\s*(?:ID|IDs|code|codes)?\s*[:=]?\s*([0-9][A-Za-z0-9]{3})\b", re.I)
REPOSITORY_DOMAINS = (
    "github.com",
    "gitlab.com",
    "zenodo.org",
    "figshare.com",
    "figshare.org",
    "osf.io",
    "dryad",
    "datadryad.org",
    "materialscloud.org",
    "nomad-lab.eu",
    "materialsproject.org",
    "catalysis-hub.org",
    "huggingface.co",
    "codeocean.com",
)
AVAILABILITY_TERMS = (
    "data availability",
    "code availability",
    "supporting information",
    "supplementary information",
    "available at",
    "available on",
    "available through",
    "provided at",
    "provided on",
    "provided through",
    "deposited in",
    "repository",
    "source data",
    "input files",
    "raw data",
)


def assess_asset_availability(
    record: dict[str, Any],
    verify_urls: bool = False,
    url_timeout_seconds: float = 6.0,
    max_urls: int = 8,
) -> dict[str, Any]:
    assets = record.get("assets") or {}
    text = _record_text(record)
    contextual_urls = list(dict.fromkeys(_contextual_urls(text) + _contextual_doi_urls(text)))
    identifiers = _external_identifiers(text)
    repository_urls = [
        url
        for url in contextual_urls
        if any(domain in url.casefold() for domain in REPOSITORY_DOMAINS)
    ]
    selected_urls = list(dict.fromkeys(repository_urls + contextual_urls))[:max_urls]
    probes = [_probe_url(url, url_timeout_seconds) for url in selected_urls] if verify_urls else []

    local = {
        "paper": _existing_path(assets.get("paper")),
        "supplementary": _existing_paths(assets.get("supplementary", [])),
        "text": _existing_paths(assets.get("text", [])),
        "hidden_reference_files": _existing_paths(assets.get("hidden_reference_files", [])),
        "visible_data": {
            mode: _existing_paths(paths)
            for mode, paths in (assets.get("visible_data") or {}).items()
        },
    }
    statements = [term for term in AVAILABILITY_TERMS if term in text.casefold()]
    structured_inputs = len(record.get("inputs", []))
    described_inputs = sum(
        1 for item in record.get("inputs", []) if _input_status(item) == "described"
    )
    reconstructible_inputs = sum(
        1 for item in record.get("inputs", []) if _input_status(item) == "reconstructible"
    )
    materialized_inputs = sum(1 for item in record.get("inputs", []) if _materialized_input(item))
    reference_evidence = len(record.get("reference_results", [])) + len(record.get("evidence", []))
    reachable = [item["url"] for item in probes if item.get("reachable")]
    reachable_repositories = [url for url in reachable if url in repository_urls]
    acquisition = _acquisition_record(record)
    explicit_status = str(acquisition.get("status") or "").casefold()
    visible_file_total = sum(len(paths) for paths in local["visible_data"].values())
    availability_state = _availability_state(
        explicit_status=explicit_status,
        materialized_inputs=materialized_inputs,
        visible_file_count=visible_file_total,
        statements=statements,
        candidate_urls=selected_urls,
        identifiers=identifiers,
        discovery_was_run=bool(acquisition.get("discovery_completed")),
    )
    mode_assessment = {}
    for mode in task_types_for_record(record) or list(TASK_TYPES):
        visible_count = len(local["visible_data"].get(mode, [])) + len(
            local["visible_data"].get("all", [])
        )
        input_score = min(1.0, (materialized_inputs + visible_count * 2) / 2)
        source_score = (
            1.0
            if reachable_repositories
            else 0.7
            if repository_urls
            else 0.4
            if statements
            else 0.0
        )
        gold_score = min(1.0, reference_evidence / 4)
        if mode == "paper_reproduction":
            score = 100 * (0.4 * input_score + 0.35 * source_score + 0.25 * gold_score)
        elif mode == "mechanistic_rule_discovery":
            score = 100 * (0.45 * input_score + 0.15 * source_score + 0.40 * gold_score)
        else:
            score = 100 * (0.55 * input_score + 0.15 * source_score + 0.30 * gold_score)
        if input_score >= 0.5 and gold_score >= 0.5:
            decision = "pass"
        elif input_score == 0 and source_score == 0:
            decision = "review"
        else:
            decision = "review"
        mode_assessment[mode] = {
            "decision": decision,
            "score": round(score, 1),
            "structured_input_count": structured_inputs,
            "described_input_count": described_inputs,
            "reconstructible_input_count": reconstructible_inputs,
            "materialized_input_count": materialized_inputs,
            "visible_file_count": visible_count,
            "reference_evidence_count": reference_evidence,
            "source_signal": round(source_score, 2),
        }

    return {
        "local_assets": local,
        "availability_statements": statements,
        "candidate_urls": selected_urls,
        "repository_urls": repository_urls,
        "url_probes": probes,
        "reachable_urls": reachable,
        "reachable_repository_urls": reachable_repositories,
        "external_identifiers": identifiers,
        "acquisition": acquisition,
        "availability_state": availability_state,
        "release_blocking": availability_state in {"confirmed_unavailable", "access_restricted"},
        "mode_assessment": mode_assessment,
        "verified_online": verify_urls,
        "status_note": _availability_note(availability_state),
    }


def preliminary_availability(document: dict[str, Any]) -> dict[str, Any]:
    text = _document_text(document)
    lower = text.casefold()
    statements = [term for term in AVAILABILITY_TERMS if term in lower]
    urls = _contextual_urls(text)
    repositories = [
        url for url in urls if any(domain in url.casefold() for domain in REPOSITORY_DOMAINS)
    ]
    if repositories:
        decision = "pass"
        score = 80.0
    elif statements:
        decision = "review"
        score = 55.0
    else:
        decision = "review"
        score = 20.0
    return {
        "decision": decision,
        "score": score,
        "availability_statements": statements,
        "candidate_repository_urls": repositories[:10],
        "reason": "metadata-level only; actual files must be verified after acquisition",
    }


def _record_text(record: dict[str, Any]) -> str:
    chunks = [record.get("central_problem", "")]
    for item in record.get("evidence", []):
        chunks.append(item.get("statement", ""))
    assets = record.get("assets") or {}
    for raw in assets.get("text", []):
        path = Path(raw)
        if path.exists():
            chunks.append(path.read_text(encoding="utf-8", errors="replace")[:2_000_000])
    return "\n".join(chunks)


def _document_text(document: dict[str, Any]) -> str:
    chunks = [document.get("title", ""), document.get("abstract", "")]
    raw = document.get("deep_text_path") or document.get("cheap_text_path")
    if raw and Path(raw).exists():
        chunks.append(Path(raw).read_text(encoding="utf-8", errors="replace")[:2_000_000])
    return "\n".join(chunks)


def _contextual_urls(text: str) -> list[str]:
    text = _repair_pdf_urls(text)
    urls = []
    for match in URL_PATTERN.finditer(text):
        start = max(0, match.start() - 240)
        end = min(len(text), match.end() + 120)
        context = text[start:end].casefold()
        url = _clean_url(match.group(0))
        if any(term in context for term in AVAILABILITY_TERMS) or any(
            domain in url.casefold() for domain in REPOSITORY_DOMAINS
        ):
            urls.append(url)
    return list(dict.fromkeys(urls))


def _repair_pdf_urls(text: str) -> str:
    repaired = text.replace("\\_", "_")
    repaired = re.sub(r"https?://(?=10\.\d{4,9}/)", "", repaired, flags=re.I)
    repaired = re.sub(
        r"(https?://[^\s<>]+\.)\s+(?=(?:com|org|net|edu|gov|io|ai|ch|uk)\b)",
        r"\1",
        repaired,
        flags=re.I,
    )
    repaired = re.sub(r"(https?://[^\s<>]+[/_-])\s+(?=[A-Za-z0-9])", r"\1", repaired)
    repaired = re.sub(r"(https?://[^\s<>]+)\s+(?=[_/-][A-Za-z0-9])", r"\1", repaired)
    return repaired


def _clean_url(value: str) -> str:
    url = value.rstrip(".,;:)")
    url = re.sub(
        r"\.(?:correspondence|results|the|we|relevant|data|source|supporting)$",
        "",
        url,
        flags=re.I,
    )
    url = re.sub(r"/(?:and|or|the)$", "/", url, flags=re.I)
    return url


def _external_identifiers(text: str) -> dict[str, list[str]]:
    repaired = _repair_pdf_urls(text)
    dois = [match.group(1).rstrip(".,;:") for match in DOI_PATTERN.finditer(repaired)]
    pdb_ids = [match.group(1).upper() for match in PDB_PATTERN.finditer(repaired)]
    return {
        "dois": list(dict.fromkeys(dois))[:20],
        "pdb_ids": list(dict.fromkeys(pdb_ids))[:20],
    }


def _contextual_doi_urls(text: str) -> list[str]:
    repaired = _repair_pdf_urls(text)
    output = []
    for match in DOI_PATTERN.finditer(repaired):
        start = max(0, match.start() - 240)
        end = min(len(repaired), match.end() + 160)
        context = repaired[start:end].casefold()
        if any(term in context for term in AVAILABILITY_TERMS):
            doi = match.group(1).rstrip(".,;:)")
            output.append(f"https://doi.org/{doi}")
    return list(dict.fromkeys(output))


def _acquisition_record(record: dict[str, Any]) -> dict[str, Any]:
    assets = record.get("assets") or {}
    raw = record.get("asset_acquisition") or assets.get("acquisition") or {}
    if isinstance(raw, str):
        return {"status": raw}
    return dict(raw) if isinstance(raw, dict) else {}


def _availability_state(
    *,
    explicit_status: str,
    materialized_inputs: int,
    visible_file_count: int,
    statements: list[str],
    candidate_urls: list[str],
    identifiers: dict[str, list[str]],
    discovery_was_run: bool,
) -> str:
    aliases = {
        "validated": "validated",
        "reference_executed": "validated",
        "materialized": "materialized",
        "acquired": "acquired_unvalidated",
        "downloaded": "acquired_unvalidated",
        "confirmed_unavailable": "confirmed_unavailable",
        "unavailable": "confirmed_unavailable",
        "access_restricted": "access_restricted",
        "restricted": "access_restricted",
    }
    if explicit_status in aliases:
        return aliases[explicit_status]
    if visible_file_count or materialized_inputs:
        return "materialized"
    if candidate_urls or identifiers.get("pdb_ids"):
        return "pending_acquisition"
    if statements:
        return "pending_discovery"
    if discovery_was_run:
        return "unresolved_after_discovery"
    return "pending_discovery"


def _availability_note(state: str) -> str:
    notes = {
        "validated": "task inputs were acquired and validated",
        "materialized": "task inputs are locally materialized but still require validation",
        "acquired_unvalidated": "external assets were acquired but have not been validated",
        "pending_acquisition": "the PDF contains an asset, repository, SI, DOI, or structure signal; acquisition has not completed",
        "pending_discovery": "only local PDF material has been inspected; external asset discovery has not completed",
        "unresolved_after_discovery": "automatic discovery completed without locating usable task assets; manual resolution is required",
        "confirmed_unavailable": "required assets were explicitly confirmed unavailable after discovery",
        "access_restricted": "required assets were located but access restrictions prevent benchmark redistribution or use",
    }
    return notes[state]


def _probe_url(url: str, timeout: float) -> dict[str, Any]:
    headers = {"User-Agent": "ResearchChemBench-data-pipeline/0.2"}
    for method in ("HEAD", "GET"):
        try:
            request = urllib.request.Request(url, headers=headers, method=method)
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return {
                    "url": url,
                    "reachable": 200 <= response.status < 400,
                    "status": response.status,
                    "final_url": response.geturl(),
                    "method": method,
                }
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as exc:
            last_error = str(exc)
    return {"url": url, "reachable": False, "error": last_error}


def _existing_path(raw: str | None) -> str | None:
    if not raw:
        return None
    path = Path(raw)
    return str(path.resolve()) if path.exists() else None


def _existing_paths(values: list[str]) -> list[str]:
    return [resolved for value in values if (resolved := _existing_path(value))]


def _materialized_input(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    status = str(
        value.get("verification_status") or value.get("availability_status") or ""
    ).casefold()
    if status in {"materialized", "validated", "reference_executed"}:
        return True
    raw_path = value.get("path") or value.get("source_path")
    if raw_path and Path(str(raw_path)).exists():
        return True
    return any(
        value.get(key) for key in ("smiles", "inchi", "coordinates", "xyz", "cif", "structure")
    )


def _input_status(value: Any) -> str:
    if not isinstance(value, dict):
        return ""
    return str(
        value.get("verification_status") or value.get("availability_status") or ""
    ).casefold()
