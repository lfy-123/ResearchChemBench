from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any, Callable

from src.core.concurrency import ordered_parallel_map
from src.core.io import sha256_file, stable_id
from src.core.logging import log_progress
from src.integrations.grobid import GrobidClient, parse_grobid_tei, text_quality
from src.integrations.mineru import run_mineru_queue

TextExtractor = Callable[[Path, Path, dict[str, Any]], str]

EVIDENCE_PATTERNS = {
    "software": re.compile(
        r"\b(?:Gaussian|ORCA|VASP|Quantum ESPRESSO|CP2K|GROMACS|LAMMPS|OpenMM|NAMD|CHARMM|Psi4|PySCF|xTB|CREST|PLUMED)\b",
        re.I,
    ),
    "parameter": re.compile(
        r"\b(?:basis set|functional|pseudopotential|plane-wave cutoff|k-point|force field|time step|temperature|pressure|ensemble|solvent model|convergence threshold|charge|multiplicity)\b",
        re.I,
    ),
    "input": re.compile(
        r"\b(?:initial structure|starting geometry|input file|coordinates?|cif file|xyz file|topology|parameter file)\b",
        re.I,
    ),
    "result": re.compile(
        r"\b(?:energy|barrier|rate constant|frequency|orbital|band gap|density of states|trajectory|radial distribution|free energy|table\s+S\d+|figure\s+S\d+)\b",
        re.I,
    ),
}


def extract_supplementary_materials(
    papers: list[dict[str, Any]],
    output_dir: str | Path,
    config: dict[str, Any],
    *,
    grobid_client: GrobidClient | None = None,
    fast_extractor: TextExtractor | None = None,
) -> list[dict[str, Any]]:
    root = Path(output_dir).expanduser().resolve()
    text_root = root / "text"
    text_root.mkdir(parents=True, exist_ok=True)
    extractor = fast_extractor or _pdftotext
    return ordered_parallel_map(
        lambda paper: _extract_paper(
            paper,
            text_root,
            config,
            grobid_client=grobid_client,
            fast_extractor=extractor,
        ),
        papers,
        max_workers=int(config.get("workers", 1)),
        on_complete=lambda completed, total, _index, paper, record: log_progress(
            "stage_06_supplementary_extraction",
            completed,
            total,
            str(paper["paper_id"]),
            status=record["supplementary_extraction"]["status"],
        ),
    )


def supplementary_extraction_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    statuses: dict[str, int] = {}
    documents = 0
    errors = 0
    for record in records:
        value = record.get("supplementary_extraction") or {}
        status = str(value.get("status") or "unknown")
        statuses[status] = statuses.get(status, 0) + 1
        documents += len(value.get("documents") or [])
        errors += len(value.get("errors") or [])
    return {"papers": len(records), "documents": documents, "errors": errors, "statuses": statuses}


def supplementary_asset_result(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Adapt Stage 01/02/06 paper files to the isolated Agent context contract."""
    assets: list[dict[str, Any]] = []
    papers: list[dict[str, Any]] = []
    for record in records:
        paper_id = str(record["paper_id"])
        papers.append(
            {
                "paper_id": paper_id,
                "status": "ready",
                "supplementary_status": (
                    record.get("supplementary_extraction") or {}
                ).get("status"),
            }
        )
        documents = [
            *(record.get("main_documents") or []),
            *((record.get("supplementary_extraction") or {}).get("documents") or []),
        ]
        for document in documents:
            source_value = document.get("source_path")
            if not source_value or not Path(source_value).is_file():
                continue
            source = Path(source_value)
            document_id = str(document.get("document_id") or stable_id("doc", str(source)))
            assets.append(
                {
                    "asset_id": stable_id("asset", paper_id, document_id, length=16),
                    "paper_id": paper_id,
                    "file_name": source.name,
                    "role": document.get("document_role") or "supplementary",
                    "relation_type": "pipeline_document",
                    "parser": document.get("parser") or "stage02",
                    "original_path": str(source.resolve()),
                    "source_local_path": str(source.resolve()),
                    "readable_paths": [document["text_path"]]
                    if document.get("text_path") and Path(document["text_path"]).is_file()
                    else [],
                    "size_bytes": source.stat().st_size,
                    "sha256": document.get("sha256") or sha256_file(source),
                }
            )
    return {
        "papers": papers,
        "assets": assets,
        "summary": {"papers": len(papers), "assets": len(assets)},
    }


def _extract_paper(paper, text_root, config, *, grobid_client, fast_extractor):
    paper_id = str(paper["paper_id"])
    documents: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    for existing in paper.get("supplementary_documents") or []:
        text_path = existing.get("text_path")
        if not text_path or not Path(text_path).is_file():
            continue
        text = Path(text_path).read_text(encoding="utf-8", errors="replace")
        document = {
            **existing,
            "parser": "stage02_reuse",
            "extraction_status": "reused_stage02",
            "newly_downloaded": False,
        }
        documents.append(document)
        evidence.extend(_extract_evidence(text, document))
    attachments = (
        (paper.get("supplementary_acquisition") or {}).get("attachments") or []
    )
    for attachment in attachments:
        if not attachment.get("newly_downloaded", True):
            continue
        source = Path(str(attachment["path"]))
        document_id = stable_id("si", paper_id, attachment.get("sha256") or str(source), length=16)
        destination = text_root / paper_id / f"{document_id}.txt"
        destination.parent.mkdir(parents=True, exist_ok=True)
        parser = "pdftotext"
        try:
            text = fast_extractor(source, destination, config)
            quality = text_quality(text, None)
            threshold = float(config.get("minimum_text_quality", 60))
            if quality["score"] < threshold and grobid_client is not None:
                tei = grobid_client.process_fulltext_document(source)
                text = parse_grobid_tei(tei)["text"]
                destination.write_text(text, encoding="utf-8")
                quality = text_quality(text, None)
                parser = "grobid"
            if quality["score"] < threshold and config.get("mineru", {}).get("execute"):
                text, mineru_record = _mineru_text(
                    source,
                    paper_id,
                    document_id,
                    text_root.parent / "mineru",
                    config["mineru"],
                )
                destination.write_text(text, encoding="utf-8")
                quality = text_quality(text, None)
                parser = "mineru"
            document = {
                "paper_id": paper_id,
                "document_id": document_id,
                "document_role": "supplementary",
                "source_path": str(source),
                "text_path": str(destination),
                "parser": parser,
                "text_quality": quality,
                "text_characters": len(text),
                "extraction_status": "success",
                "newly_downloaded": True,
            }
            if parser == "mineru":
                document["mineru"] = mineru_record
            documents.append(document)
            evidence.extend(_extract_evidence(text, document))
        except Exception as exc:
            errors.append(
                {
                    "paper_id": paper_id,
                    "document_id": document_id,
                    "source_path": str(source),
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
    if errors and documents:
        status = "partial"
    elif errors:
        status = "si_parse_error"
    elif attachments:
        status = "success"
    elif documents:
        status = "reused_stage02"
    else:
        status = "no_supplementary"
    by_type = {
        kind: [item for item in evidence if item["evidence_type"] == kind]
        for kind in EVIDENCE_PATTERNS
    }
    return {
        **paper,
        "supplementary_extraction": {
            "status": status,
            "documents": documents,
            "errors": errors,
            "evidence": evidence,
            "software_evidence": by_type["software"],
            "parameter_evidence": by_type["parameter"],
            "input_evidence": by_type["input"],
            "result_evidence": by_type["result"],
        },
        "pipeline_routing": {
            **(paper.get("pipeline_routing") or {}),
            "stage_06": status,
            "continue": True,
        },
    }


def _pdftotext(source: Path, destination: Path, config: dict[str, Any]) -> str:
    completed = subprocess.run(
        [str(config.get("pdftotext_command", "pdftotext")), "-layout", str(source), str(destination)],
        capture_output=True,
        text=True,
        timeout=int(config.get("pdftotext_timeout_seconds", 300)),
        check=False,
    )
    if completed.returncode != 0 or not destination.is_file():
        raise RuntimeError(completed.stderr[-1000:] or f"pdftotext exited {completed.returncode}")
    text = destination.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        raise RuntimeError("pdftotext produced empty output")
    return text


def _mineru_text(source, paper_id, document_id, root, config):
    queue = [
        {
            "document_id": document_id,
            "paper_id": paper_id,
            "source_path": str(source),
            "title": source.stem,
            "expected_pages": None,
        }
    ]
    records = run_mineru_queue(
        queue,
        root,
        execute=True,
        command=config.get("command", "mineru"),
        method="auto",
        backend=config.get("backend"),
        timeout_seconds=int(config.get("timeout_seconds", 3600)),
        working_directory=config.get("working_directory"),
        environment=config.get("environment"),
        extra_args=config.get("extra_args"),
        reuse_existing=bool(config.get("reuse_existing", True)),
        min_markdown_chars=int(config.get("min_markdown_chars", 100)),
        stage_name="stage_06_supplementary_mineru",
    )
    record = records[0]
    markdown = record.get("markdown_path")
    if record.get("status") not in {"success", "reused"} or not markdown:
        raise RuntimeError(record.get("error") or f"MinerU status: {record.get('status')}")
    return Path(markdown).read_text(encoding="utf-8", errors="replace"), record


def _extract_evidence(text: str, document: dict[str, Any]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for kind, pattern in EVIDENCE_PATTERNS.items():
        for match in pattern.finditer(text):
            start = max(0, match.start() - 120)
            end = min(len(text), match.end() + 120)
            output.append(
                {
                    "document_id": document.get("document_id"),
                    "source": document.get("source_path"),
                    "evidence_type": kind,
                    "matched_text": match.group(0),
                    "character_start": match.start(),
                    "character_end": match.end(),
                    "snippet": " ".join(text[start:end].split()),
                }
            )
    return output
